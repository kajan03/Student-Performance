import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import train




x_test=[[10,0,0,20,80]]
train.regressor.built = True
train.regressor.load_weights("model.h5")
new_prediction = train.regressor.predict(x_test)
print(new_prediction)
