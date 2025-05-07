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
                    string(credentialsId: 'skeleton_api_host', variable: 'SKELETON_API_HOST'),
                    string(credentialsId: 'skeleton_api_port', variable: 'SKELETON_API_PORT'),
                ]) {
                    script {
                        def envContent = """SKELETON_API_HOST=${env.SKELETON_API_HOST}
                                            SKELETON_API_PORT=${env.SKELETON_API_PORT}
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

		stage('Build and deploy docker image') {
			steps {
				echo 'Building the Docker image...'
				sh './d.compose.sh'
				echo 'Deployment completed successfully.'
			}
		}

// 		stage('Deploy completed - Set flag') {
//             steps {
//                 script {
//                     writeFile file: '/tmp/skeleton_api_status.flag', text: 'SUCCESS'
//                     echo 'Wrote build completion flag.'
//                 }
//             }
//         }

	}
}