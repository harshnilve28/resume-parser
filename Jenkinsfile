pipeline {
    agent any
    stages {
        stage('Install Python') {
            steps {
                sh '''
                apt-get update -y
                apt-get install -y python3 python3-pip
                '''
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest'
            }
        }
        stage('Run Pylint') {
            steps {
                sh 'pip3 install pylint && pylint *.py'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t resume-parser .'
            }
        }
    }
}
