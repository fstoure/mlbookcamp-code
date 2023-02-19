import pickle
import numpy as np

from flask import Flask, request, jsonify


def predict_single(customer, dv, model):
    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[:, 1]
    return y_pred[0]


with open('churn-model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


app = Flask('churn')

@app.route('/')
def index():
    return 'Welcome to the Churn Prediction API'


@app.route('/predict', methods=['GET', 'POST'])
def predict_api():
    if request.method == 'POST':
        customer = request.get_json()

        prediction = predict_single(customer, dv, model)
        churn = prediction >= 0.5

        result = {
            'churn_probability': float(prediction),
            'churn': bool(churn),
        }

        return jsonify(result)
    else:
        return 'Please use POST method to get prediction.'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)