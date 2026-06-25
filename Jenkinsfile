pipeline {
    agent any
    environment {
        REGISTRY_ID = '<ИДЕНТИФИКАТОР_ВАШЕГО_РЕЕСТРА>'
        IMAGE_NAME  = "cr.yandex/${REGISTRY_ID}/sber-app:latest"
    }
    triggers {
        pollSCM('* * * * *')
    }
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Docker Build & Push') {
            steps {
                // Авторизуемся в Яндексе, собираем и пушим образ
                withCredentials([usernamePassword(credentialsId: 'yandex-registry-cred', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh "echo \$DOCKER_PASSWORD | docker login --username \$DOCKER_USERNAME --password-stdin cr.yandex"
                    sh "docker build -t ${IMAGE_NAME} ."
                    sh "docker push ${IMAGE_NAME}"
                }
            }
        }
        
        stage('K8s Deployment') {
            steps {
                // Разворачиваем приложение в кластере в неймспейсе sber-app
                // с использованием созданного на самом первом шаге секрета ycr-secret
                sh """
                kubectl apply -n sber-app -f - «EOF
                apiVersion: apps/v1
                kind: Deployment
                metadata:
                  name: sber-app-deployment
                spec:
                  replicas: 2
                  selector:
                    matchLabels:
                      app: sber-web-app
                  template:
                    metadata:
                      labels:
                        app: sber-web-app
                    spec:
                      containers:
                      - name: web-app
                        image: ${IMAGE_NAME}
                        ports:
                        - containerPort: 8080
                      imagePullSecrets:
                      - name: ycr-secret
EOF
                """
            }
        }
    }
}
