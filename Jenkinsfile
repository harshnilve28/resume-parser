pipeline {
    agent any
    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python -m pytest
                '''
            }
        }

        stage('Run Pylint') {
            steps {
                sh '''
                . venv/bin/activate
                pip install pylint
                pylint *.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t resume-parser .'
            }
        }
    }
}
