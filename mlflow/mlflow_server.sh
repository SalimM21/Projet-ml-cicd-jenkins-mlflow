#!/usr/bin/env bash
# simple MLflow server (backend: sqlite local, artifact root: ./mlruns)
mkdir -p mlruns
export MLFLOW_BACKEND_STORE_URI="sqlite:///mlflow.db"
export MLFLOW_ARTIFACT_ROOT="./mlruns"
mlflow server --backend-store-uri ${MLFLOW_BACKEND_STORE_URI} \
--default-artifact-root ${MLFLOW_ARTIFACT_ROOT} \
--host 0.0.0.0 --port 5000