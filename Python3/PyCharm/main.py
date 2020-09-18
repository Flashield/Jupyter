import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import datasets


iris = datasets.load_iris()
list(iris.keys())

print(type(iris))

X = iris.data[:, 2:4]
y = (iris.target == 2).astype(np.int)

log_reg = LogisticRegression(solver="liblinear", C=10**10, random_state=55)
log_reg.fit(X, y)

x0, x1 = np.meshgrid(
        np.linspace(2.9, 7, 500).reshape(-1, 1),
        np.linspace(0.8, 2.7, 200).reshape(-1, 1),
    )
X_new = np.c_[x0.ravel(), x1.ravel()]


