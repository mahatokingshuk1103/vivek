pipeline {
    agent any

    // Define variables for Docker image and tag
    environment {
        imageName = "kingshuk0311/siemens"
        imageTag = "v${env.BUILD_ID}"
        dockerfile = "./Dockerfile"
        
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
                    withCredentials([string(credentialsId: 'dockerhubpwd', variable: 'dockerhubpwd')]) {
                        sh "sudo docker login -u kingshuk0311 -p \${dockerhubpwd}"
                    }

                    // Push the Docker image to Docker Hub
                    sh "sudo docker push ${imageName}:${imageTag}"
                }
            }
        }

       stage('Deploy to Kubernetes') {
    steps {
        script {
            withAWS(credentials: 'AWSID', region: 'us-east-2') {
                sh 'aws eks update-kubeconfig --name my-eks-cluster2'
                sh 'kubectl delete pods --all -n prod2'
                sh "sed -i 's|{{IMAGE_TAG}}|${imageName}:${imageTag}|' mydeployment.yaml"
                sh 'kubectl apply -f mydeployment.yaml --namespace=prod2'
            }
        }
    }

    }
}
