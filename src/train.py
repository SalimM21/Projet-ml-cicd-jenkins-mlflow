# src/train.py
import os
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


MLFLOW_URI = os.environ.get('MLFLOW_TRACKING_URI', 'http://localhost:5000')
mlflow.set_tracking_uri(MLFLOW_URI)
mlflow.set_experiment('Iris_Classifier')


if __name__ == '__main__':
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)


n_estimators = int(os.environ.get('N_ESTIMATORS', 100))


with mlflow.start_run():
model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)


mlflow.log_param('n_estimators', n_estimators)
mlflow.log_metric('accuracy', acc)


# Save model as artifact and register
mlflow.sklearn.log_model(model, artifact_path='model')


print(f'Accuracy: {acc}')
run_id = mlflow.active_run().info.run_id
print(f'Logged to MLflow with run_id={run_id}')


# Optional: register model in MLflow Model Registry (requires backend support)
try:
model_uri = f'runs:/{run_id}/model'
mlflow.register_model(model_uri, 'IrisRandomForest')
print('Model registered in MLflow Model Registry (if available).')
except Exception as e:
print('Model registration skipped or failed:', e)