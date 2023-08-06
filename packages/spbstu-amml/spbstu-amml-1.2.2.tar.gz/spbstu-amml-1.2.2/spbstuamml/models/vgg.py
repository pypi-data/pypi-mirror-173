import tensorflow as tf

from .. import hubutils

VGG16 = tf.keras.applications.vgg16.VGG16

VGG19 = tf.keras.applications.vgg19.VGG19


def vgg16_from_hub(dataset: str) -> VGG16:
    dh = hubutils.DSHalper(dataset)
    
    return tf.keras.models.load_model(dh.get_model_path("vgg16.h5"))


def vgg19_from_hub(dataset: str) -> VGG19:
    dh = hubutils.DSHalper(dataset)

    return tf.keras.models.load_model(dh.get_model_path("vgg19.h5"))