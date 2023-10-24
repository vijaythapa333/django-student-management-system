pipeline {
    agent any
    
    stages {
        stage('Fetch code') {
            steps {
                git 'https://github.com/PranitRout07/django-student-management-system.git'
            }
        }
        stage('Code Analysis') {
            environment {
                scannerHome = tool 'sonar4.7'
            }
            steps {
                  withSonarQubeEnv('sonar') {
                      bat '%scannerHome%\\bin\\sonar-scanner -Dsonar.projectKey=student-management-system ' +
                        '-Dsonar.projectName=student-management-system ' +
                        '-Dsonar.projectVersion=1.0 ' +
                        '-Dsonar.sources=. '
               
              }
            }

        }
        stage('Docker build image'){
            steps{
                
                bat 'docker build -t student-management-system .'
                
            }

        }
        stage('Push docker image to dockerhub'){
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'dockerPass', usernameVariable: 'dockerUser')]) {
                   bat "docker login -u ${env.dockerUser} -p ${env.dockerPass}"
                   bat "docker tag student-management-system ${env.dockerUser}/student-management-system:latest"
                   bat "docker push ${env.dockerUser}/student-management-system:latest "
                }
            }

        }
        stage('scan with trivy') {
            steps {
            
                bat "docker run --rm -v D:/trivy-report/:/root/.cache/ aquasec/trivy:0.18.3 image pranit007/student-management-system"
            }

        }
        stage('Run minikube'){
            steps{
                
                bat 'minikube start'
            }

        }

        stage('run deploy and service'){
            
            steps{
               
                    bat 'kubectl apply -f Deployment.yaml'
                    bat 'kubectl apply -f service.yaml'
                
                
            }

            
        }
        stage('Introduce a 130-Second Delay') {
            steps {
                // Sleep for 130 seconds , to give enough time for pods up and running
                sleep time: 130, unit: 'SECONDS'
            }

        }
        stage('Run the service') {
            steps {
                script {
                    try {
                        timeout(time: 60, unit: 'SECONDS') {
                            bat 'minikube service my-service'
                        }
                    } catch (Exception e) {
                        echo "Timeout occurred, but handling it as SUCCESS"
                    }
                }
            }
        }
    }
        post {
        always {
            script {
                def textColor
                switch (currentBuild.currentResult) {
                    case 'SUCCESS':
                        textColor = 'green';
                        break
                    default:
                        textColor = 'red';
                }

                emailext (
                    subject: "pipeline status: ${currentBuild.currentResult}",
                    body: """<html>
                                <body>
                                    <p><b>Project:</b> <i>${JOB_NAME}</i></p>
                                    <p><b>Build Number:</b> <i>${BUILD_NUMBER}</i></p>
                                    <p><b>Build URL:</b> ${BUILD_URL}</p>
                                    <p style='color: ${textColor};'>Build Result: ${currentBuild.currentResult}</p>
                                </body>
                            </html>""",
                    to: 'pranitrout72@gmail.com',
                    from: 'jenkins@example.com',
                    replyTo: 'jenkins@example.com',
                    mimeType: 'text/html'
                )
            }
        }
    }
}
