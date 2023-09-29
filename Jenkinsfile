pipeline {
    agent any

    // Define variables for Docker image and tag
    environment {
        imageName = "kingshuk0311/siemens"
        imageTag = "v${env.BUILD_ID}"
        dockerfile = "./Dockerfile"
        SSH_CREDENTIALS = credentials('kopssiemensid')  // Replace with your SSH credential ID
        KOPS_CLUSTER_NAME = 'kingshuk.shop'
        KOPS_INSTANCE_IP = 'ip-172.31.32.55' 
    }

    
    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'main', credentialsId: 'gitid', url: 'https://github.com/mahatokingshuk1103/vivek.git'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the defined variables
                    sh "sudo -S docker build -t ${imageName}:${imageTag} -f ${dockerfile} ."
                    echo "${imageName}:${imageTag}"
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                script {
                    // Log in to Docker Hub using credentials
                    withCredentials([string(credentialsId: 'dockerhub', variable: 'dockerhubpwd')]) {
                        sh "sudo docker login -u kingshuk0311 -p \${dockerhubpwd}"
                    }

                    // Push the Docker image to Docker Hub
                    sh "sudo docker push ${imageName}:${imageTag}"
                }
            }
        }

        stage('Deploy to EKS') {
            
            steps {
                script {
                  sh 'kubectl apply -f kubernetes/deployment.yaml' 
                }
            }
        }
    }
}
