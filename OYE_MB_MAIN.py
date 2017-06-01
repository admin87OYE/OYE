import data_analisis as da
from matplotlib import style
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from sklearn import preprocessing, svm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def main():
    df = pd.read_csv("C:\\Users\\Andrija\\Desktop\\adlog.csv")
    df = df[['value', 'pct_change', 'mean', 'median']]
    forecast_col = 'value'
    df.fillna(-99999, inplace=True)
    forecast_out = 6  # int(math.ceil(0.001 * len(df)))
    df['label'] = df[forecast_col].shift(-forecast_out)
    df.dropna(inplace=True)

    X = np.array(df)
    # X = preprocessing.scale(X)
    X = X[:-forecast_out]
    X_lately = X[-forecast_out:]

    df.dropna(inplace=True)
    y = np.array(df['label'])
    y = np.array(df['label'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01)

    clf = LinearRegression(n_jobs=-1)
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)

    print(accuracy)


main()
