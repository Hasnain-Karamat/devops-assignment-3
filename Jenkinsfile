pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '--user root -v /dev/shm:/dev/shm'
        }
    }
    environment {
        INSTRUCTOR_EMAIL = 'qasimalik@gmail.com'
    }
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Install Chrome & Dependencies') {
            steps {
                sh '''
                    apt-get update && apt-get install -y wget gnupg curl
                    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
                    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
                    apt-get update && apt-get install -y google-chrome-stable
                    pip install --upgrade pip
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                    pip install pytest selenium webdriver-manager
                '''
            }
        }
        stage('Run Selenium Tests') {
            steps {
                sh 'python -m pytest tests/test_login.py -v --tb=short'
            }
        }
    }
    post {
        always {
            emailext (
                subject: "DevOps Assignment 3: Build ${currentBuild.fullDisplayName} - ${currentBuild.result}",
                body: "Pipeline Status: ${currentBuild.result}. View logs at: ${env.BUILD_URL}",
                to: "${env.INSTRUCTOR_EMAIL}",
                from: "cadethasnainkaramat@gmail.com"
            )
        }
    }
}
