pipeline {
    agent any

    environment {
        PROJECT_NAME      = "skeleton_api_testing"
        IMAGE_NAME        = "skeleton_api_test"
        NETWORK_NAME      = "skeleton_api"
        REPORTS_HOST_DIR  = "${WORKSPACE}/reports"
    }

    stages {

        stage('Clone repository') {
            steps {
                checkout scm
            }
        }

//         stage('Check for changes') {
//             when {
//                 changeset "**"
//             }
//             steps {
//                 echo 'Changes detected – proceeding with pipeline.'
//             }
//         }

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

        stage('Ensure Docker network exists') {
            steps {
                sh '''
                    docker network inspect ${NETWORK_NAME} >/dev/null 2>&1 || \
                    docker network create ${NETWORK_NAME}
                '''
            }
        }

        stage('Reset previous stack') {
            steps {
                echo 'Cleaning previous compose stack'
                sh '''
                    docker compose --env-file .env -p ${PROJECT_NAME} down --remove-orphans || true
                '''
            }
        }

        stage('Build image & run tests') {
            steps {
                echo 'Building image and executing pytest inside docker‑compose...'
                script {
                    def exitCode = sh(
                        script: '''
                            set -e
                            docker compose --env-file .env -p ${PROJECT_NAME} \
                              up --build --abort-on-container-exit --exit-code-from test_runner
                        ''',
                        returnStatus: true
                    )
                    if (exitCode != 0) {
                        error "Test container exited with status ${exitCode}"
                    }
                }
            }
        }

        stage('Generate Allure HTML') {
            steps {
                echo 'Generating Allure HTML report...'
                sh '''
                    docker run --rm \
                      -v ${REPORTS_HOST_DIR}:/app/reports \
                      ${IMAGE_NAME} \
                      allure generate /app/reports/allure-results \
                                     -o /app/reports/allure-report --clean
                '''
            }
        }

        stage('Validate report generation') {
            steps {
                sh 'ls -R reports'
            }
        }

        stage('Archive HTML report') {
            steps {
                archiveArtifacts artifacts: 'reports/allure-report/**', allowEmptyArchive: false
            }
        }

        stage('Clean up containers') {
            steps {
                echo 'Stopping and removing containers...'
                sh 'docker compose --env-file .env -p ${PROJECT_NAME} down --remove-orphans || true'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}