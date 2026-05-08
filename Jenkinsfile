pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '--user root -v /dev/shm:/dev/shm'
        }
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    apt-get update && apt-get install -y wget gnupg curl
                    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
                    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
                    apt-get update && apt-get install -y google-chrome-stable
                    
                    pip install --upgrade pip
                    pip install -r requirements.txt
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
                subject: "Build ${currentBuild.fullDisplayName} - ${currentBuild.currentResult}",
                body: '''
                    <h2>Pipeline Status: ${BUILD_STATUS}</h2>
                    <p><b>Job:</b> ${JOB_NAME}</p>
                    <p><b>Build:</b> ${BUILD_NUMBER}</p>
                    <p><b>Commit:</b> ${GIT_COMMIT}</p>
                    <p>Full Logs: <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                ''',
                to: '${GIT_COMMITTER_EMAIL}',
                from: 'jenkins@devops-assignment.com'
            )
        }
    }
}
