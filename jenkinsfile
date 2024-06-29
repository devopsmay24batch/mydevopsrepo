pipeline {
    agent any

    environment {
        registryCredentials = 'dockerhub_credentials'
        dockerImage = 'sandeshyashlaha/devopsproject2/pythonapp'
        dockerTag = 'latest'
        dockerfilePath = 'Dockerfile'  // Assuming Dockerfile is at the root of the repository
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from GitHub
                git 'https://github.com/sandeshdevops/mydevopsrepo1.git'
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
                // Example: Run tests inside the Docker container
                script {
                    dockerImage.inside {
                        sh 'python test.py'  // Adjust this command based on your actual test script
                    }
                }
            }
        }

        stage('Push') {
            steps {
                // Push Docker image to Docker Hub
                script {
                    docker.withRegistry('https://registry.hub.docker.com', registryCredentials) {
                        dockerImage.push()
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Docker image built, tested, and pushed successfully.'
        }
        failure {
            echo 'Pipeline failed! Check the Jenkins console output for details.'
        }
    }
}
