import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, Imputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib


train_data = pd.read_csv("application_train.csv")
test_data = pd.read_csv("application_test.csv")


le = LabelEncoder()
for col in train_data:
    if train_data[col].dtype == "object" and len(train_data[col].unique()) <= 2:
        train_data[col] = le.fit_transform(train_data[col])
        if col in test_data:
            test_data[col] = le.transform(test_data[col])

train_data = pd.get_dummies(train_data)
test_data = pd.get_dummies(test_data)


train_labels = train_data["TARGET"]
train_data, test_data = train_data.align(test_data, join="inner", axis=1)
train_data["TARGET"] = train_labels


imputer = Imputer(strategy="median")
scaler = MinMaxScaler(feature_range=(0, 1))

train_data = train_data.drop(columns=["TARGET"])
train_data = imputer.fit_transform(train_data)
train_data = scaler.fit_transform(train_data)


X_train, X_valid, y_train, y_valid = train_test_split(
    train_data, train_labels, test_size=0.2, random_state=42
)


model = LogisticRegression(C=0.0001)
model.fit(X_train, y_train)


joblib.dump(model, "saved_models/logistic_regression_model.pkl")
joblib.dump(imputer, "saved_models/imputer.pkl")
joblib.dump(scaler, "saved_models/scaler.pkl")
joblib.dump(train_data.columns, "saved_models/columns.pkl")
