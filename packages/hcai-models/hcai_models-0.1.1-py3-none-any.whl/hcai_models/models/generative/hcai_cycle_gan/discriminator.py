from keras.layers import Flatten, Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.models import Model
from keras_contrib.layers import InstanceNormalization


def d_layer(layer_input, filters, f_size=4, normalization=True):
    """Discriminator layer"""
    d = Conv2D(filters, kernel_size=f_size, strides=2, padding="same")(layer_input)
    d = LeakyReLU(alpha=0.2)(d)
    if normalization:
        d = InstanceNormalization()(d)
    return d


def build_discriminator(img_shape, df, normalize: bool = False):

    img = Input(shape=img_shape)

    d1 = d_layer(img, df, normalization=False)
    d2 = d_layer(d1, df * 2)
    d3 = d_layer(d2, df * 4)
    d4 = d_layer(d3, df * 8)
    # d5 = d_layer(d4, df * 16)

    if normalize:
        validity = Conv2D(1, kernel_size=4, strides=1, padding="same", activation="tanh")(d4)
        validity = (validity + 1) / 2
    else:
        validity = Conv2D(1, kernel_size=4, strides=1, padding="same")(d4)

    return Model(img, validity)
