#!/usr/bin/env bash
# Charger image dans minikube et deploy
IMAGE=local/iris-ml-app:local
docker build -t $IMAGE .
minikube image load $IMAGE
kubectl apply -f k8s/mlflow-deployment.yaml
kubectl apply -f k8s/mlflow-service.yaml
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml
kubectl get pods