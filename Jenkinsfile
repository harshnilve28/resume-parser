pipeline {
    agent any
    stages {

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

        stage('Run Tests') {
            steps {
                sh 'PYTHONPATH=. venv/bin/pytest'
            }
        }

        stage('Run Pylint') {
            steps {
                sh 'venv/bin/pylint app.py db.py || true'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t resume-parser .'
            }
        }
    }
}
