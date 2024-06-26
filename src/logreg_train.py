import numpy as np
from numpy import ndarray
import argparse
from DataFrame import DataFrame
import pickle

def softmax(x: ndarray):
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / np.sum(e_x, axis=-1, keepdims=True)

class LogisticRegression:

    def __init__(self, lr=0.15, epochs=100, n_classes=4):
        self.lr = lr
        self.epochs = epochs
        self.w = None
        self.b = None
        self.n_classes = n_classes

    def fit(self, X: ndarray, y: ndarray):
        n_samples, n_features = X.shape
        y_encoded = np.zeros((n_samples, self.n_classes))
        y_encoded[np.arange(n_samples), y] = 1

        self.w = np.zeros((n_features, self.n_classes))
        self.b = np.zeros((1, self.n_classes))

        for _ in range(self.epochs):
            y_pred_linear = np.dot(X, self.w) + self.b
            y_pred = softmax(y_pred_linear)

            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y_encoded))
            db = (1 / n_samples) * np.sum(y_pred - y_encoded, axis=0)

            self.w = self.w - self.lr * dw
            self.b = self.b - self.lr * db

    def predict(self, X):
        y_pred_linear = np.dot(X, self.w) + self.b
        y_pred = softmax(y_pred_linear)
        class_pred = np.argmax(y_pred, axis=1)
        return class_pred


def preprocess(df: DataFrame):
    y = df._columns["Hogwarts House"]
    y = np.array([0 if x == "Ravenclaw" else 1 if x == "Slytherin" else 2 if x == "Gryffindor" else 3 for x in y._data])

    df.drop_non_numerical(index=False)
    df.fillna_with_mean()
    X = df.scale_features()
    X = np.array(list(zip(
        X["Astronomy"],
        X["Herbology"],
        X["Charms"],
        X["Ancient Runes"],
        X["Defense Against the Dark Arts"],
        X["Divination"],
    )))
    return X, y


def get_features():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    args = parser.parse_args()
    df = DataFrame()
    df.read_csv(args.path)
    return preprocess(df)


def main():
    X, y = get_features()
    lr = LogisticRegression()
    lr.fit(X, y)
    with open("model.pkl", "wb") as file:
        pickle.dump(lr, file)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)