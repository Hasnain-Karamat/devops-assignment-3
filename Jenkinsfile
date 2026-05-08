pipeline {
    agent any
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "====================================="
                    echo "Installing Dependencies..."
                    echo "====================================="
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r requirements.txt
                    python3 -m pip install pytest selenium webdriver-manager
                '''
            }
        }
        
        stage('Run Selenium Tests') {
            steps {
                sh '''
                    echo "====================================="
                    echo "Running Selenium Tests..."
                    echo "====================================="
                    python3 -m pytest tests/test_login.py -v --tb=short
                '''
            }
        }
    }
    
    post {
        always {
            echo "====================================="
            echo "PIPELINE FINISHED - RESULT: ${currentBuild.currentResult}"
            echo "====================================="
        }
    }
}
