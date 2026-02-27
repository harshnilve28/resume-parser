pipeline {
    agent any

    environment {
        IMAGE_NAME = "resume-parser"
        DOCKERHUB_REPO = "harshnilve/resume-parser"
        AZURE_VM_IP = "10.0.0.5"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                rm -rf venv
                python3 -m venv venv
                venv/bin/pip install --upgrade pip
                venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pylint') {
            steps {
                sh 'venv/bin/pylint app.py db.py || true'
            }
        }

        stage('Run Pytest') {
            steps {
                sh 'PYTHONPATH=. venv/bin/pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker tag $IMAGE_NAME $DOCKERHUB_REPO:latest
                    docker push $DOCKERHUB_REPO:latest
                    '''
                }
            }
        }

        stage('Deploy to Azure VM') {
            steps {
                sshagent(['azure-vm-ssh']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no azureuser@$AZURE_VM_IP "
                    docker pull $DOCKERHUB_REPO:latest &&
                    docker stop resume-parser || true &&
                    docker rm resume-parser || true &&
                    docker run -d -p 5000:5000 --name resume-parser $DOCKERHUB_REPO:latest
                    "
                    '''
                }
            }
        }

    }
}
