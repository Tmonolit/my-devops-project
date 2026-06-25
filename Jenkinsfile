pipeline {
    agent {
        kubernetes {
            yaml '''
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: kaniko
                image: gcr.io/kaniko-project/executor:debug
                command:
                - sleep
                args:
                - 9999999
              - name: kubectl
                image: dtzar/helm-kubectl:latest
                command:
                - sleep
                args:
                - 9999999
            '''
        }
    }
    
    environment {
        // Ваш ID реестра уже вписан
        REGISTRY_ID = 'crpch0cjeu3o3a0vqps4'
        IMAGE_NAME  = "cr.yandex/${REGISTRY_ID}/sber-app:18"
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
        
        stage('Build & Push (Kaniko)') {
            steps {
                container('kaniko') {
                    withCredentials([usernamePassword(credentialsId: 'yandex-registry-cred', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                        sh '''
                        mkdir -p /kaniko/.docker
                        
                        # Профессиональный подход: кодируем связку логин:пароль в Base64
                        AUTH=$(echo -n "$USER:$PASS" | base64 | tr -d '\n' | tr -d '\r')
                        
                        # Безопасно записываем закодированный ключ
                        echo '{"auths": {"cr.yandex": {"auth": "'$AUTH'"}}}' > /kaniko/.docker/config.json
                        
                        # Запускаем сборку
                        /kaniko/executor --context `pwd` --dockerfile `pwd`/Dockerfile --destination $IMAGE_NAME
                        '''
                    }
                }
            }
        }
        
        stage('K8s Deployment') {
            steps {
                container('kubectl') {
                    sh '''
                    cat <<EOF > deploy.yaml
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
                    kubectl apply -n sber-app -f deploy.yaml
                    '''
                }
            }
        }
    }
}
