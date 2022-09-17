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

data = pd.read_csv('RNN Dataset.csv',usecols=["Grade","Subject","Section","Marks","Total","Performance"])
# creating an encoder
le = LabelEncoder()
data['Section'] = le.fit_transform(data['Section'])
data['Section'].value_counts()
data['Subject'] = le.fit_transform(data['Subject'])
data['Subject'].value_counts()
x=data.iloc[:, :5]
y = data.iloc[:,5]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2) 
sc = StandardScaler()

x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)


regressor=Sequential()
regressor.add(LSTM(units=100,return_sequences=True,input_shape=(x_train.shape[1], 1)))
regressor.add(Dropout(0.4))
regressor.add(LSTM(units=100,return_sequences=True,input_shape=(x_train.shape[1], 1)))
regressor.add(Dropout(0.4))
regressor.add(LSTM(units=100,return_sequences=True,input_shape=(x_train.shape[1], 1)))
regressor.add(Dropout(0.4))
regressor.add(LSTM(units=100,return_sequences=True,input_shape=(x_train.shape[1], 1)))
regressor.add(Dropout(0.4))

regressor.add(Dense(units=1))

regressor.compile(optimizer='adam',loss='mean_squared_error',metrics=['accuracy'])
regressor.fit(x_train,y_train,epochs=10,batch_size=32,shuffle=True)

regressor.save_weights("model.h5")

