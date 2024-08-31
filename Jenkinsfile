pipeline {
    agent any

    environment {
        registryCredentials = '271bdd6e-0a51-49bb-9140-bf91dcea0235'
        dockerImage = 'sandeshyashlaha/devopsproject2'
        dockerTag = 'latest'
        dockerfilePath = 'docker/creating-image/Dockerfile'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from GitHub
                git branch: 'main', url: 'https://github.com/sandeshdevops/mydevopsrepo1.git'
            }
        }

        stage('Build') {
            steps {
                // Build Docker image
                script {
                    dockerImage = docker.build("${dockerImage}:${dockerTag}", "-f ${dockerfilePath} .")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    dockerImage.inside('-p 5001:5000') {
                        sh 'python3 docker/creating-image/app.py --host=0.0.0.0 &'
                        sleep 10
                    }
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', registryCredentials) {
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Approval') {
            steps {
                script {
                    input message: 'Approve deployment?', ok: 'Deploy'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Debug information
                    sh 'docker ps -a'
                    sh 'docker images'

                    // Stop and remove existing container if it exists
                    sh """
                    if [ \$(docker ps -a -q -f name=project2) ]; then
                        docker stop project2 || true
                        docker rm project2 || true
                    fi
                    """

                    // Run Docker container
                    sh "docker run -d -p 8081:80 --name project2 ${env.dockerImage}:${env.dockerTag}"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Docker image built, tested, pushed, and deployed successfully.'
        }
        failure {
            echo 'Pipeline failed! Check the Jenkins console output for details.'
        }
    }
}
