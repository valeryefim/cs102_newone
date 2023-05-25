import csv
import string

import numpy as np
from bayes import NaiveBayesClassifier

with open("/Users/valery/Desktop/cs102_newone/homework07/data/SMSSpamCollection") as f:
    data = list(csv.reader(f, delimiter="\t"))


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    s = s.translate(translator).lower().strip()
    if not s:
        return None
    return s


X, y = [], []
for i, j in data:
    X.append(j)
    y.append(i)

X_train, y_train, X_test, y_test = np.array(X[:3900]), np.array(y[:3900]), np.array(X[3900:]), np.array(y[3900:])

# print(len(y))
# print(len(X))

model = NaiveBayesClassifier(alpha=1)
model.fit(X_train, y_train)

print(model.score(X_test, y_test))
