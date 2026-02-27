pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/harshnilve28/resume-parser.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
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
