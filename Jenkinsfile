pipeline {
    agent any

    tools {
        jdk 'JDK11'
        maven 'Maven3'
        python 'Python3'
    }

    environment {
        VENV_DIR = 'venv'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo/mixed-project.git'
            }
        }

        // ---------------- JAVA STAGES ----------------
        stage('Java - Build') {
            when {
                expression { fileExists('pom.xml') }
            }
            steps {
                sh 'mvn clean compile'
            }
        }

        stage('Java - Test') {
            when {
                expression { fileExists('pom.xml') }
            }
            steps {
                sh 'mvn test'
            }
        }

        stage('Java - Package') {
            when {
                expression { fileExists('pom.xml') }
            }
            steps {
                sh 'mvn package'
            }
        }

        // ---------------- PYTHON STAGES ----------------
        stage('Python - Setup') {
            when {
                expression { fileExists('requirements.txt') }
            }
            steps {
                sh '''
                python -m venv $VENV_DIR
                . $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Python - Test') {
            when {
                expression { fileExists('requirements.txt') }
            }
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                pytest || true
                '''
            }
        }

        stage('Python - Package') {
            when {
                expression { fileExists('setup.py') }
            }
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                python setup.py sdist
                '''
            }
        }

        // ---------------- ARCHIVE ----------------
        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: '''
                    target/*.jar,
                    dist/**,
                    **/*.log
                ''', fingerprint: true
            }
        }
    }

    post {
        success {
            echo '✅ Java & Python Pipeline Successful'
        }
        failure {
            echo '❌ Pipeline Failed'
        }
        always {
            cleanWs()
        }
    }
}
