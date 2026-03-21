pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Java Build') {
            steps {
                sh 'mvn --version || true'
            }
        }

        stage('Python Run') {
            steps {
                sh 'python3 --version || true'
            }
        }
    }
}
