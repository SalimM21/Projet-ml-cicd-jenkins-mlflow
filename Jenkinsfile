pipeline {
agent any


environment {
DOCKER_IMAGE = "${env.DOCKER_REGISTRY ?: 'local'}/iris-ml-app:${env.BUILD_NUMBER}"
MLFLOW_URI = credentials('MLFLOW_URI') // or set as env var on Jenkins
}


stages {
stage('Checkout') {
steps { checkout scm }
}


stage('Setup Python') {
steps {
sh 'python3 -m venv venv || true'
sh '. venv/bin/activate && pip install -r src/requirements.txt'
}
}


stage('Train (MLflow)') {
steps {
withEnv(["MLFLOW_TRACKING_URI=${MLFLOW_URI}", "N_ESTIMATORS=100"]) {
sh '. venv/bin/activate && python src/train.py'
}
}
}


stage('Build Docker Image') {
steps {
sh 'docker build -t ${DOCKER_IMAGE} .'
}
}


stage('Push Docker Image') {
steps {
withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
sh 'docker push ${DOCKER_IMAGE}'
}
}
}


stage('Deploy to Kubernetes') {
steps {
// Assumes kubectl configured on agent
sh 'kubectl set image deployment/iris-ml-app iris-ml-app=${DOCKER_IMAGE} --record || kubectl apply -f k8s/app-deployment.yaml'
sh 'kubectl apply -f k8s/app-service.yaml || true'
}
}
}


post {
success { echo 'Pipeline finished successfully.' }
failure { echo 'Pipeline failed.' }
}
}