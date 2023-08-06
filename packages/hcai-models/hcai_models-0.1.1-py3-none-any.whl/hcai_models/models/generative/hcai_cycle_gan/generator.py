from keras.layers import Conv2DTranspose
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Input, Concatenate
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import UpSampling2D, Conv2D
from tensorflow.keras.models import Model

from keras_contrib.layers import InstanceNormalization


def conv2d(layer_input, filters, f_size=4):
    """Layers used during downsampling"""
    d = Conv2D(filters, kernel_size=f_size, strides=2, padding="same")(layer_input)
    d = LeakyReLU(alpha=0.2)(d)
    d = InstanceNormalization()(d)
    return d


def deconv2d(layer_input, skip_input, filters, f_size=4, dropout_rate=0):
    """Layers used during upsampling"""

    u = UpSampling2D(size=2)(layer_input)
    u = Conv2D(
        filters, kernel_size=f_size, strides=1, padding="same", activation="relu"
    )(u)

    # u = Conv2DTranspose(filters, kernel_size=f_size, strides=2, padding="same", activation="relu")(layer_input)

    if dropout_rate:
        u = Dropout(dropout_rate)(u)
    u = InstanceNormalization()(u)
    u = Concatenate()([u, skip_input])
    return u


def build_generator(img_shape, gf, channels):
    """U-Net Generator"""

    # Image input
    d0 = Input(shape=img_shape)

    # Downsampling
    d1 = conv2d(d0, gf)
    d2 = conv2d(d1, gf * 2)
    d3 = conv2d(d2, gf * 4)
    d4 = conv2d(d3, gf * 8)

    # Upsampling
    u1 = deconv2d(d4, d3, gf * 4)
    u2 = deconv2d(u1, d2, gf * 2)
    u3 = deconv2d(u2, d1, gf)

    u4 = UpSampling2D(size=2)(u3)
    output_img = Conv2D(
        channels, kernel_size=4, strides=1, padding="same", activation="tanh"
    )(u4)

    output_img = (output_img + 1) / 2

    return Model(d0, output_img)
