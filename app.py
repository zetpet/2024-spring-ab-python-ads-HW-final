from flask import Flask, request, jsonify
import joblib
import pandas as pd
from prometheus_flask_exporter import PrometheusMetrics


model = joblib.load("saved_models/logistic_regression_model.pkl")
imputer = joblib.load("saved_models/imputer.pkl")
scaler = joblib.load("saved_models/scaler.pkl")
columns = joblib.load("saved_models/columns.pkl")

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route("/predict", methods=["POST"])
@metrics.counter("predict_requests", "Number of prediction requests")
def predict():
    data = request.get_json(force=True)
    df = pd.DataFrame(data, index=[0])
    df = df.reindex(columns=columns, fill_value=0)

    df = imputer.transform(df)
    df = scaler.transform(df)
    prediction = model.predict_proba(df)[:, 1]

    return jsonify({"prediction": float(prediction[0])})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
