pipeline {
    agent any

    environment {
        PROJECT_NAME = 'skeleton_api_testing'
        IMAGE_NAME = 'skeleton_api_testing_image'
        CONTAINER_NAME = 'skeleton_api_testing_container'
        NETWORK_NAME = 'skeleton_api'
        ALLURE_VERSION = '2.27.0'
    }

    stages {

        stage('Clone repository') {
            steps {
                echo 'Cloning the repository...'
                checkout scm
                echo 'Repository cloned successfully.'
            }
        }

        stage('Prepare environment variables') {
            steps {
                withCredentials([
                    string(credentialsId: 'QA_IP',   variable: 'QA_IP'),
                    string(credentialsId: 'QA_PORT', variable: 'QA_PORT')
                ]) {
                    sh '''
                        cat > .env <<EOF
                        QA_IP=${QA_IP}
                        QA_PORT=${QA_PORT}
                        EOF
                    '''
                }
            }
        }

        stage('Ensure docker network exists') {
            steps {
                echo "Checking if Docker network '${env.NETWORK_NAME}' exists..."
                sh '''
                    if ! docker network inspect ${NETWORK_NAME} >/dev/null 2>&1; then
                        echo "Docker network '${NETWORK_NAME}' not found. Creating it..."
                        docker network create ${NETWORK_NAME}
                    else
                        echo "Docker network '${NETWORK_NAME}' already exists."
                    fi
                '''
            }
        }

        stage('Build docker image') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run tests in container') {
            steps {
                sh """
                    docker run --name ${CONTAINER_NAME} \\
                        --env-file .env \\
                        --network ${NETWORK_NAME} \\
                        -v "\${PWD}/reports:/app/reports" \\
                        ${IMAGE_NAME}
                """
            }
        }

        stage('Validate if any report was generated as of now') {
            steps {
                sh 'ls -R reports'
            }
        }

        stage('Fix Permissions') {
            steps {
                sh 'chmod -R a+rw reports/allure-report || true'
            }
        }

        stage('Generate Allure report') {
            steps {
                sh """
                    docker run --rm \\
                        -v "\${PWD}/reports:/app/reports" \\
                        ${IMAGE_NAME} \\
                        /opt/allure-${ALLURE_VERSION}/bin/allure generate /app/reports/allure-results -o /app/reports/allure-report --clean
                """
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-report']]
            }
        }

    }

    post {
        always {
            script {
                // Cleanup container (if exists)
                sh "docker rm -f ${CONTAINER_NAME} || true"
            }
        }
    }
}