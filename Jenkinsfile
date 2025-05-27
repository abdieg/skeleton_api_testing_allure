pipeline {
	agent any

	stages {

		stage('Clone repository') {
			steps {
				echo 'Cloning the repository...'
				git url: 'https://github.com/abdieg/skeleton_api_testing.git', branch: 'main'
				echo 'Repository cloned successfully.'
			}
		}

		stage('Check for changes') {
			steps {
			    echo 'Check for changes is commented because testing suite can be executed on demand.'
// 				script {
// 					def changes = sh(script: 'git log -1 --pretty=format:"%h"', returnStdout: true).trim()
// 					def buildTriggerFile = '.last_build_commit'
//
// 					if (fileExists(buildTriggerFile)) {
// 						def lastBuildCommit = readFile(buildTriggerFile).trim()
// 						if (changes == lastBuildCommit) {
// 							echo "No changes since last build. Skipping deployment."
// 							currentBuild.result = 'SUCCESS'
// 							// Stop further stages
// 							error("Pipeline aborted: no changes detected.")
// 						}
// 					}
//
// 					// Save latest commit hash for next run
// 					writeFile file: buildTriggerFile, text: changes
// 				}
			}
		}

		stage('Prepare environment variables') {
            steps {
                withCredentials([
                    string(credentialsId: 'QA_IP', variable: 'QA_IP'),
                    string(credentialsId: 'QA_PORT', variable: 'QA_PORT'),
                ]) {
                    script {
                        def envContent = """QA_IP=${env.QA_IP}
                                            QA_PORT=${env.QA_PORT}
                                            """
                        writeFile file: '.env', text: envContent
                        echo "Created .env file with hidden environment variables."
                    }
                }
            }
        }

		stage('Set Permissions') {
			steps {
				echo 'Setting execute permissions on scripts...'
				sh 'chmod +x ./d.compose.sh'
				echo 'Permissions set successfully.'
			}
		}

// 		stage('Clean previous reports') {
// 			steps {
// 				echo 'Cleaning previous reports...'
// 				sh 'rm -rf reports && mkdir -p reports'
// 			}
// 		}

		stage('Build and deploy docker image') {
			steps {
				echo 'Running the testing container with pytest...'
				script {
					def exitCode = sh(script: './d.compose.sh', returnStatus: true)
					if (exitCode != 0)
					{
						error("Tests failed with exit code ${exitCode}")
					}
					else
					{
						echo "Tests passed successfully."
					}
				}
			}
		}

		stage('Validate report generation') {
			steps {
				echo 'Check if report was generated...'
				sh 'pwd'
				sh 'ls -l'
				sh 'cd reports'
			    sh 'ls -l reports'
			}
		}

        stage('Archive HTML report') {
			steps {
				echo 'Archiving pytest HTML report...'
				archiveArtifacts artifacts: 'reports/pytest_report_*.html', allowEmptyArchive: false
			}
		}

		stage('Clean up containers') {
			steps {
				echo 'Stopping and removing containers...'
				sh 'docker compose --env-file .env -p skeleton_api_testing down --remove-orphans || true'
			}
		}

	}
}