import pandas as pd;
import numpy as np;
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def performance_predict(marks):
    df = pd.read_csv("algebra.csv",usecols = ['Algebra'])

    df['total'] = ((df['Algebra']/25)*100)

    y = df['total']
    x = df[df.columns.difference(['total'])]

    labels = ['weaknesss','strength']
    bins =[0,50,100]
    y = pd.cut(y, bins, labels = labels)

    test_size = 0.3
    seed = 42
    x_train,x_test,y_train,y_test = train_test_split(x,y, test_size = test_size, random_state = seed,stratify=y)
    y_train.value_counts(normalize=True)

    model = DecisionTreeClassifier (random_state=10)

    model.fit(x_train,y_train)

    x_test = np.array(marks)
    x_test = x_test.reshape((-1,1))

    return model.predict(x_test)
