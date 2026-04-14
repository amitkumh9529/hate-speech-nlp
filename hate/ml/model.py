# Creating model architecture.
from hate.entity.config_entity import ModelTrainerConfig
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import LSTM,Activation,Dense,Dropout,Input,Embedding,SpatialDropout1D
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.metrics import BinaryAccuracy
from hate.constants import *

class ModelArchitecture:

    def __init__(self):
        pass

    
    def get_model(self):
        model = Sequential()
        model.add(Embedding(MAX_WORDS, 100,input_length=MAX_LEN))
        model.add(SpatialDropout1D(0.2))
        model.add(LSTM(100,dropout=0.2,recurrent_dropout=0.2))
        model.add(Dense(1))  # No sigmoid — using from_logits=True for numerical stability
        model.build(input_shape=(None, MAX_LEN))
        model.summary()
        model.compile(
            loss=BinaryCrossentropy(from_logits=True),
            optimizer=RMSprop(),
            metrics=[BinaryAccuracy(threshold=0.0, name="accuracy")]
        )

        return model
