pipeline {

    agent any

    parameters {
        string(
        name: 'PYTEST_MARKER',
        defaultValue: 'main',
        description: 'Choose the marker to run: smoke, regression, main, schema, data_types, data_ranges, data_parameters, data_sanitization, authentication, permission, e2e'
        )
    }

    environment {
        PROJECT_NAME = 'skeleton_api_testing'
        IMAGE_NAME = 'skeleton_api_testing_image'
        CONTAINER_NAME = 'skeleton_api_testing_container'
        NETWORK_NAME = 'skeleton_api'
        REPORTS_DIR = 'reports'
    }

    tools {
        allure 'allure'
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
                echo "Running tests with marker: ${params.PYTEST_MARKER}"
                sh '''
                    docker run --name ${CONTAINER_NAME} \
                        --env-file .env \
                        --network ${NETWORK_NAME} \
                        -v "${PWD}/reports:/app/reports" \
                        -e PYTEST_MARKER="${PYTEST_MARKER}" \
                        ${IMAGE_NAME}
                '''
            }
        }

        stage('Fix report permissions') {
            steps {
                sh '''
                    docker run --rm \
                        -v "$PWD/reports:/data" \
                        alpine chown -R $(id -u):$(id -g) /data || true
                '''
            }
        }

        stage('Validate if any report was generated as of now') {
            steps {
                sh 'ls -R reports || true'
            }
        }

        stage('Generate Allure Report') {
            when {
                expression {
                    fileExists("${REPORTS_DIR}/allure-results")
                }
            }
            steps {
                // Clean old report directory to avoid AccessDeniedException
                sh 'rm -rf reports/allure-report || true'
                sh 'allure generate ${REPORTS_DIR}/allure-results -o ${REPORTS_DIR}/allure-report --clean'
            }
        }

        stage('Publish Allure Report in Jenkins') {
            steps {
                allure includeProperties: false, results: [[path: "${REPORTS_DIR}/allure-results"]]
            }
        }

    }

    post {
        always {
            script {
                sh "docker rm -f ${CONTAINER_NAME} || true"
            }
        }
    }
}