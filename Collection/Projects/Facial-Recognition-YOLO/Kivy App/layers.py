# Imports
from tensorflow.keras.layers import Layer
import tensorflow as tf

# L1 Distance Layer

class L1Dist(Layer):
    def __init__(self, **kwargs):
        super().__init__()
    
    def call(self, inp_embedding, val_embedding):
        return tf.math.abs(inp_embedding - val_embedding)