pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/harshnilve28/resume-parser.git'
            }
        }

        stage('Install Python') {
            steps {
                sh '''
                apt-get update
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
                sh 'pylint *.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t resume-parser .'
            }
        }

    }
}
