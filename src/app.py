# src/app.py
import os
import mlflow
import mlflow.sklearn
from flask import Flask, request, jsonify


MODEL_URI = os.environ.get('MODEL_URI', 'model')
MLFLOW_URI = os.environ.get('MLFLOW_TRACKING_URI', 'http://localhost:5000')
mlflow.set_tracking_uri(MLFLOW_URI)


app = Flask(__name__)


# Load model from local file saved at build-time or from MLflow
MODEL_PATH = os.environ.get('MODEL_PATH', '/app/model/model.pkl')


# If MLflow model registry URI is provided, load model from MLflow
MLFLOW_MODEL = os.environ.get('MLFLOW_MODEL')


if MLFLOW_MODEL:
print('Loading model from MLflow:', MLFLOW_MODEL)
model = mlflow.sklearn.load_model(MLFLOW_MODEL)
else:
import pickle
with open(MODEL_PATH, 'rb') as f:
model = pickle.load(f)


@app.route('/health', methods=['GET'])
def health():
return jsonify(status='ok')


@app.route('/predict', methods=['POST'])
def predict():
data = request.get_json()
if not data or 'features' not in data:
return jsonify(error='payload must contain features'), 400
features = data['features']
try:
pred = model.predict([features]).tolist()
return jsonify(prediction=pred)
except Exception as e:
return jsonify(error=str(e)), 500


if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)