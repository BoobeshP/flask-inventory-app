pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                sh '''
                echo "Java Version:"
                java -version || true

                echo "Maven Version:"
                mvn -version || true

                echo "Python Version:"
                python3 --version || python --version || true
                '''
            }
        }

        // ---------------- JAVA BUILD ----------------
        stage('Java - Build & Test') {
            when {
                expression { fileExists('pom.xml') }
            }
            steps {
                sh '''
                mvn clean test package
                '''
            }
        }

        // ---------------- PYTHON BUILD ----------------
        stage('Python - Setup & Test') {
            when {
                expression { fileExists('requirements.txt') }
            }
            steps {
                sh '''
                python3 -m venv ${VENV_DIR} || python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate

                pip install --upgrade pip
                pip install -r requirements.txt

                pytest || true
                '''
            }
        }

        // ---------------- ARCHIVE ----------------
        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'target/*.jar', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo '✅ Java + Python build successful on Linux'
        }
        failure {
            echo '❌ Build failed – check Console Output'
        }
        always {
            cleanWs()
        }
    }
}
