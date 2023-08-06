import numpy as np
import tensorflow as tf
from tensorflow.keras import activations, initializers, regularizers
from tensorflow.keras.layers import Layer


class Condenser(Layer):
    def __init__(self,
                 n_sample_points=15,
                 sampling_bounds=(-1, 100),
                 reducer_dim=None,
                 reducer_trainable=False,
                 theta_trainable=True,
                 attention_initializer="glorot_uniform",
                 bias_initializer="zeros",
                 attention_regularizer=None,
                 theta_regularizer=None,
                 bias_regularizer=None,
                 reducer_regularizer=None,
                 attention_activation="leaky_relu",
                 residual_activation=None,
                 reducer_activation=None,
                 use_residual=False,
                 use_reducer=True,
                 scalers_trainable=True,
                 attention_type="fc",
                 characteristic_dropout=0,
                 **kwargs):
        super().__init__(**kwargs)

        self.n_sample_points = n_sample_points
        self.sampling_bounds = sampling_bounds
        self.reducer_dim = reducer_dim
        self.reducer_trainable = reducer_trainable
        self.theta_trainable = theta_trainable
        self.scalers_trainable = scalers_trainable
        self.characteristic_dropout = characteristic_dropout

        self.attention_initializer = initializers.get(attention_initializer)
        self.bias_initializer = initializers.get(bias_initializer)

        self.attention_activation = activations.get(attention_activation)
        self.residual_activation = activations.get(residual_activation)
        self.reducer_activation = activations.get(reducer_activation)

        self.attention_regularizer = regularizers.get(attention_regularizer)
        self.theta_regularizer = regularizers.get(theta_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)
        self.reducer_regularizer = regularizers.get(reducer_regularizer)

        self.use_residual = use_residual
        self.use_reducer = use_reducer
        self.attention_type = attention_type

    def get_config(self):
        config = super().get_config()
        config.update({
            "n_sample_points": self.n_sample_points,
            "sampling_bounds": self.sampling_bounds,
            "reducer_dim": self.reducer_dim,
            "reducer_trainable": self.reducer_trainable,
            "theta_trainable": self.theta_trainable,
            "attention_initializer": initializers.serialize(
                self.attention_initializer),
            "bias_initializer": initializers.serialize(self.bias_initializer),
            "attention_activation": activations.serialize(
                self.attention_activation),
            "residual_activation": activations.serialize(
                self.residual_activation),
            "reducer_activation": activations.serialize(
                self.reducer_activation),
            "attention_regularizer": regularizers.serialize(
                self.attention_regularizer),
            "theta_regularizer": regularizers.serialize(
                self.theta_regularizer),
            "bias_regularizer": regularizers.serialize(self.bias_regularizer),
            "reducer_regularizer": regularizers.serialize(
                self.reducer_regularizer),
            "use_residual": self.use_residual,
            "use_reducer": self.use_reducer,
            "attention_type": self.attention_type
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    @staticmethod
    def get_custom_objects():
        return {'Condenser': Condenser}

    def build(self, input_shape):
        tf.keras.initializers.GlorotNormal(seed=0)

        in_dim = input_shape[2]
        self.input_dim = in_dim

        # attention weights
        if self.attention_type == "weighted":
            self.att_weights = self.add_weight(
                shape=[in_dim, in_dim], name="att_weights",
                initializer=self.attention_initializer,
                regularizer=self.attention_regularizer)
            self.att_bias = self.add_weight(shape=[1, in_dim],
                                            name="att1_bias",
                                            initializer=self.bias_initializer,
                                            regularizer=self.bias_regularizer)
        elif self.attention_type == "fc":
            self.att1 = self.add_weight(shape=[in_dim, in_dim],
                                        name="att1",
                                        initializer=self.attention_initializer,
                                        regularizer=self.attention_regularizer)

            self.att2 = self.add_weight(shape=[in_dim, in_dim],
                                        name="att2",
                                        initializer=self.attention_initializer,
                                        regularizer=self.attention_regularizer)
            # attention biases
            self.att1_bias = self.add_weight(shape=[1, in_dim],
                                             name="att1_bias",
                                             initializer=self.bias_initializer,
                                             regularizer=self.bias_regularizer)

            self.att2_bias = self.add_weight(shape=[1, in_dim],
                                             name="att2_bias",
                                             initializer=self.bias_initializer,
                                             regularizer=self.bias_regularizer)

        self.att_temperature = self.add_weight(shape=[1],
                                               name="att_temperature",
                                               initializer="ones")

        # characteristic function sampling points
        self.theta = self.add_weight(
            shape=[1, in_dim, self.n_sample_points], name="theta",
            initializer=tf.random_uniform_initializer(*self.sampling_bounds),
            regularizer=self.theta_regularizer,
            trainable=self.theta_trainable)

        # scalers
        self.scale_theta = self.add_weight(shape=[1],
                                           name="scale_theta",
                                           initializer="ones",
                                           trainable=self.scalers_trainable)

        self.scale_input = self.add_weight(shape=[1],
                                           name="scale_input",
                                           initializer="ones",
                                           trainable=self.scalers_trainable)

        if self.use_reducer:
            reducer_in_shape = 2 * in_dim * self.n_sample_points
            reducer_dim = (
                in_dim if self.reducer_dim is None else self.reducer_dim)
            self.reducer = self.add_weight(
                shape=[reducer_in_shape, reducer_dim],
                name="reducer",
                initializer=initializers.Orthogonal(),
                regularizer=self.reducer_regularizer,
                trainable=self.reducer_trainable)
            self.scale_reducer = self.add_weight(
                shape=[1],
                name="scale_reducer",
                initializer="ones",
                trainable=self.scalers_trainable)
            self.bias_reducer = self.add_weight(
                shape=[reducer_dim],
                name="bias_reducer",
                initializer=self.bias_initializer,
                regularizer=self.bias_regularizer)

    def compute_mask(self, _, mask=None):
        return None

    def _compute_fc_attention_scores(self, input, mask):
        # compute attention weights for all dimensions
        logits = self.attention_activation(
            tf.matmul(input, self.att1) + self.att1_bias)
        logits = self.attention_activation(
            tf.matmul(logits, self.att2) + self.att2_bias)

        # max trick for numerical stability
        logits *= self.att_temperature
        logits_max = tf.reduce_max(logits, axis=1, keepdims=True)
        ai = tf.exp(logits - logits_max)

        # ensure attention weights are null on masked values
        if mask is not None:
            mask = tf.expand_dims(tf.cast(mask, tf.float32), -1)
            ai *= mask

        ai_sum = tf.reduce_sum(ai, axis=1, keepdims=True)
        ai_sum = tf.clip_by_value(ai_sum, 1e-4, float("inf"))

        att_weights = ai / ai_sum
        att_weights = tf.expand_dims(att_weights, axis=-1)
        return att_weights

    def _compute_fc_ragged_attention_scores(self, input):
        a = tf.ragged.map_flat_values(tf.matmul, input, self.att1)
        logits = self.attention_activation(a + self.att1_bias)
        b = tf.ragged.map_flat_values(tf.matmul, logits, self.att2)
        logits = self.attention_activation(b + self.att2_bias)

        # max trick for numerical stability
        logits *= self.att_temperature
        logits_max = tf.reduce_max(logits, axis=1, keepdims=True)
        ai = tf.exp(logits - logits_max)

        ai_sum = tf.reduce_sum(ai, axis=1, keepdims=True)
        ai_sum = tf.clip_by_value(ai_sum, 1e-4, float("inf"))

        att_weights = ai / ai_sum
        att_weights = tf.expand_dims(att_weights, axis=-1)
        return att_weights

    def _compute_weighted_attention_scores(self, input, mask):
        logits = tf.matmul(input, self.att_weights)
        logits = self.attention_activation(logits + self.att_bias)

        # max trick for numerical stability
        logits *= self.att_temperature
        logits_max = tf.reduce_max(logits, axis=1, keepdims=True)
        ai = tf.exp(logits - logits_max)

        if mask is not None:
            mask = tf.expand_dims(tf.cast(mask, tf.float32), -1)
            ai *= mask

        att_weights = ai / tf.reduce_sum(ai, axis=1, keepdims=True)
        att_weights = tf.expand_dims(att_weights, -1)
        return att_weights

    def _compute_weighted_ragged_attention_scores(self, input, mask):
        logits = tf.ragged.map_flat_values(tf.matmul, input, self.att_weights)
        logits = self.attention_activation(logits + self.att_bias)

        # max trick for numerical stability
        logits *= self.att_temperature
        logits_max = tf.reduce_max(logits, axis=1, keepdims=True)
        ai = tf.exp(logits - logits_max)

        if mask is not None:
            mask = tf.expand_dims(tf.cast(mask, tf.float32), -1)
            ai *= mask

        att_weights = ai / tf.reduce_sum(ai, axis=1, keepdims=True)
        att_weights = tf.expand_dims(att_weights, -1)
        return att_weights

    def call(self, input, mask=None):
        is_ragged = isinstance(input, tf.RaggedTensor)
        if self.attention_type == "fc":
            if is_ragged:
                att_weights = self._compute_fc_ragged_attention_scores(input)
            else:
                att_weights = self._compute_fc_attention_scores(input, mask)
        elif self.attention_type == "weighted":
            if is_ragged:
                att_weights = self._compute_weighted_ragged_attention_scores(
                    input, mask)
            else:
                att_weights = self._compute_weighted_attention_scores(
                    input, mask)

        # sample characteristic function
        theta = self.theta * self.scale_theta
        phi = (tf.expand_dims(input, axis=-1)) * theta
        real = tf.reduce_sum(att_weights * tf.cos(phi), axis=1)
        imag = tf.reduce_sum(att_weights * tf.sin(phi), axis=1)

        # stack real and imaginary parts
        stack = tf.concat([real, imag], axis=-1)
        stack = tf.reshape(
            stack, (-1, 2*self.input_dim*self.n_sample_points))
        if self.characteristic_dropout > 0:
            stack = tf.keras.layers.Dropout(.1)(stack)

        # reducer output dim
        if self.use_reducer:
            stack = self.reducer_activation(
                self.scale_reducer * tf.matmul(stack, self.reducer)
                + self.bias_reducer)

        # concatenate characteristic function and input vector
        if self.use_residual:
            res = self.residual_activation(
                tf.reduce_sum(input * att_weights[:, :, :, 0], axis=1))
            stack = tf.concat([stack, res], axis=-1)
        return stack


class MultiHeadCondenser(Layer):
    def __init__(self,
                 n_heads=2,
                 hidden_dim=32,
                 hidden_activation="tanh",
                 hidden_regularizer="l2",
                 n_sample_points=15,
                 sampling_bounds=(-1, 100),
                 dropout=0,
                 characteristic_dropout=0,
                 reducer_dim=None,
                 reducer_trainable=False,
                 theta_trainable=True,
                 attention_initializer="glorot_uniform",
                 bias_initializer="zeros",
                 attention_regularizer=None,
                 theta_regularizer=None,
                 bias_regularizer=None,
                 reducer_regularizer=None,
                 attention_activation="leaky_relu",
                 residual_activation=None,
                 reducer_activation=None,
                 use_residual=False,
                 use_reducer=True,
                 scalers_trainable=True,
                 attention_type="fc",
                 **kwargs):
        super().__init__(**kwargs)
        self.dropout = dropout
        self.denses = [
            tf.keras.layers.Dense(
                hidden_dim,
                activation=hidden_activation,
                kernel_regularizer=hidden_regularizer)
            for _ in range(n_heads)
        ]
        self.condensers = [
            Condenser(
                n_sample_points=n_sample_points,
                sampling_bounds=sampling_bounds,
                reducer_dim=reducer_dim,
                reducer_trainable=reducer_trainable,
                theta_trainable=theta_trainable,
                attention_initializer=attention_initializer,
                bias_initializer=bias_initializer,
                attention_regularizer=attention_regularizer,
                theta_regularizer=theta_regularizer,
                bias_regularizer=bias_regularizer,
                reducer_regularizer=reducer_regularizer,
                attention_activation=attention_activation,
                residual_activation=residual_activation,
                reducer_activation=reducer_activation,
                use_residual=use_residual,
                use_reducer=use_reducer,
                scalers_trainable=scalers_trainable,
                attention_type=attention_type,
                characteristic_dropout=characteristic_dropout)
            for _ in range(n_heads)
        ]

    def call(self, inputs):
        results = []
        for i in range(len(self.condensers)):
            x = self.denses[i](inputs)
            if self.dropout:
                x = tf.keras.layers.Dropout(self.dropout)(x)
            x = self.condensers[i](x)
            results.append(x)
        return tf.concat(results, axis=-1)


class WeightedAttention(Layer):
    def __init__(
            self,
            hidden_dim=32,
            bias_regularizer=None,
            attention_initializer="glorot_normal",
            attention_activation="leaky_relu",
            attention_regularizer=None,
            attention_type="weighted",
            **kwargs):

        super().__init__(**kwargs)
        self.hidden_dim = hidden_dim

        self.bias_regularizer = regularizers.get(bias_regularizer)

        self.attention_initializer = initializers.get(attention_initializer)
        self.attention_activation = activations.get(attention_activation)
        self.attention_regularizer = regularizers.get(attention_regularizer)
        self.attention_type = attention_type

    def build(self, input_shape):
        dim = int(input_shape[-1])
        self.scale = dim**.5
        if self.attention_type == "fc":
            self.att1 = self.add_weight(
                name="att1",
                shape=(dim, self.hidden_dim),
                initializer=self.attention_initializer,
                regularizer=self.attention_regularizer)
            self.att2 = self.add_weight(
                name="att2",
                shape=(self.hidden_dim, 1),
                initializer=self.attention_initializer,
                regularizer=self.attention_regularizer)
            # attention biases
            self.att1_bias = self.add_weight(shape=[1, self.hidden_dim],
                                             name="att1_bias",
                                             initializer="zeros")
            self.att2_bias = self.add_weight(shape=[1],
                                             name="att2_bias",
                                             initializer="zeros")
            self.att_temperature = self.add_weight(shape=[1],
                                                   name="att_temperature",
                                                   initializer="ones")
        elif self.attention_type == "weighted":
            self.att_weights = self.add_weight(
                shape=[dim, 1], name="att_weights",
                initializer=self.attention_initializer,
                regularizer=self.attention_regularizer)

    def compute_mask(self, _, mask=None):
        return None

    def _compute_fc_attention_scores(self, input, mask):
        # compute attention weights for all dimensions
        logits = self.attention_activation(
            tf.matmul(input, self.att1) / self.scale + self.att1_bias)
        logits = tf.tanh(
            tf.matmul(logits, self.att2) / self.scale + self.att2_bias)

        # max trick for numerical stability
        logits *= self.att_temperature
        logits_max = tf.reduce_max(logits, axis=1, keepdims=True)
        ai = tf.exp(logits - logits_max)

        # ensure attention weights are null on masked values
        if mask is not None:
            mask = tf.expand_dims(tf.cast(mask, tf.float32), -1)
            ai *= mask

        ai_sum = tf.reduce_sum(ai, axis=1, keepdims=True)
        ai_sum = tf.clip_by_value(ai_sum, 1e-4, float("inf"))

        att_weights = ai / ai_sum
        return att_weights

    def _compute_fc_ragged_attention_scores(self, inp):
        a = tf.ragged.map_flat_values(tf.matmul, inp, self.att1)
        logits = self.attention_activation(a / self.scale + self.bias[0])
        b = tf.ragged.map_flat_values(tf.matmul, logits, self.att2)
        logits = self.attention_activation(b / self.scale + self.bias[1])

        logits *= self.att_temperature
        logits_max = tf.reduce_max(logits, axis=1, keepdims=True)
        att_weights = tf.exp(logits - logits_max)
        att_weights_sum = tf.reduce_sum(att_weights, axis=1, keepdims=True)
        att_weights /= tf.clip_by_value(att_weights_sum, 1e-4, float("inf"))
        return att_weights

    def _compute_weighted_attention_scores(self, input, mask):
        logits = tf.matmul(input, self.att_weights)
        # max trick for numerical stability
        logits_max = tf.reduce_max(logits, axis=1, keepdims=True)
        att_weights = tf.exp(logits - logits_max)

        if mask is not None:
            mask = tf.expand_dims(tf.cast(mask, tf.float32), -1)
            att_weights *= mask

        att_weights_sum = tf.reduce_sum(att_weights, axis=1, keepdims=True)
        att_weights /= tf.clip_by_value(
            att_weights_sum, 1e-4, float("inf"))
        return att_weights

    def _compute_weighted_ragged_attention_scores(self, input, mask):
        logits = tf.ragged.map_flat_values(tf.matmul, input, self.att_weights)
        # max trick for numerical stability
        logits_max = tf.reduce_max(logits, axis=1, keepdims=True)
        att_weights = tf.exp(logits - logits_max)

        if mask is not None:
            mask = tf.expand_dims(tf.cast(mask, tf.float32), -1)
            att_weights *= mask

        att_weights_sum = tf.reduce_sum(att_weights, axis=1, keepdims=True)
        att_weights /= tf.clip_by_value(
            att_weights_sum, 1e-4, float("inf"))
        return att_weights

    def call(self, inp, mask=None):
        is_ragged = isinstance(inp, tf.RaggedTensor)
        if self.attention_type == "fc":
            if is_ragged:
                att_weights = self._compute_fc_ragged_attention_scores(inp)
            else:
                att_weights = self._compute_fc_attention_scores(inp, mask)
        elif self.attention_type == "weighted":
            if is_ragged:
                att_weights = self._compute_weighted_ragged_attention_scores(
                    inp, mask)
            else:
                att_weights = self._compute_weighted_attention_scores(
                    inp, mask)
        result = tf.math.reduce_sum(inp * att_weights, axis=1, keepdims=False)
        return result

    def get_config(self):
        config = super(WeightedAttention, self).get_config()
        config.update({"hidden_dim": self.hidden_dim,
                       "bias_regularizer": self.bias_regularizer,
                       "attention_initializer": self.attention_initializer,
                       "attention_activation": self.attention_activation,
                       "attention_regularizer": self.attention_regularizer})
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)


class SelfAttention(Layer):
    def __init__(
            self,
            attention_activation="tanh",
            attention_width=12,
            use_positional_encoding=False,
            **kwargs):

        super().__init__(**kwargs)
        self.attention_activation = tf.keras.activations.get(
            attention_activation)
        self.attention_width = attention_width
        self.use_positional_encoding = use_positional_encoding

    def build(self, input_shape):
        self.input_length = input_shape[1]
        dim = input_shape[2]
        self.K = self.add_weight(shape=(dim, dim),
                                 initializer="glorot_normal")

        self.temperature = self.add_weight(shape=(1,),
                                           initializer="ones")

        self.bias = self.add_weight(shape=(1,), initializer="zeros")

        if self.use_positional_encoding:
            # self.positional_encoding = positional_encoding(
            #     input_shape[1], input_shape[2])
            self.positional_encoding = self.add_weight(
                shape=(input_shape[1], input_shape[2]),
                initializer="glorot_normal")

    def compute_mask(self, _, mask=None):
        return mask

    def _compute_attention(self, input):
        if self.use_positional_encoding:
            key = tf.matmul(input, self.K) + self.positional_encoding
            positional_input = input + self.positional_encoding
            logits = tf.matmul(key, positional_input,
                               transpose_b=True) + self.bias
        else:
            key = tf.matmul(input, self.K)
            logits = tf.matmul(key, input, transpose_b=True) + self.bias[0]
        return self.attention_activation(logits)

    def _compute_ragged_attention(self, input):
        key = tf.ragged.map_flat_values(tf.matmul, input, self.K)
        logits = tf.matmul(key, input, transpose_b=True) + self.bias[0]
        logits += self.bias[0]
        return self.attention_activation(logits)

    def call(self, input, mask=None):
        is_ragged = isinstance(input, tf.RaggedTensor)
        if not is_ragged:
            logits = self._compute_attention(input)
            input_length = input.shape[1]
            if self.attention_width is not None:
                lower = np.arange(0, input_length) - \
                    self.attention_width // 2
                lower = tf.expand_dims(lower, axis=-1)
                upper = lower + self.attention_width
                indices = tf.expand_dims(
                    np.arange(0, input_length), axis=0)
                logits -= 10000.0 * \
                    (1.0 - tf.cast(lower <= indices, tf.float32)
                     * tf.cast(indices < upper, tf.float32))
            if mask is not None:
                mask = tf.expand_dims(tf.cast(mask, tf.float32), axis=-1)
                logits -= 10000.0 * (
                    (1.0 - mask) * (1.0 - tf.keras.backend.permute_dimensions(
                        mask, (0, 2, 1))))
        else:
            logits = self._compute_ragged_attention(input)

        logits *= self.temperature
        logits_max = tf.reduce_max(logits, keepdims=True, axis=-1)
        scores = tf.exp(logits - logits_max)
        scores /= tf.reduce_sum(scores, axis=-1, keepdims=True)

        combination = tf.matmul(scores, input)
        return combination
