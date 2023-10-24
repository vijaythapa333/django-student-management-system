# PIPELINE
![diagram-export-10-24-2023-7_25_50-PM](https://github.com/PranitRout07/django-student-management-system/assets/102309095/54ea742e-e016-474a-957c-caa65f0177b0)

# Tools Used

##### Github
##### Sonarqube
##### Docker
##### DockerHub
##### Minikube
##### Jenkins

# Explaination
_First code is fetched from the github.Then code analysis is done using sonarqube to find any kind of bugs , duplicate codes or security vulnerabilities in code. After this 
docker image is build and that docker image is pushed to my own dockerhub account . Then image scanning is done by using Trivy. Then started a minikube cluster locally using docker
as driver . The deployment.yaml and service.yaml runs and a 130 sec delay is added so that the pods and services can be up and running . As i am using docker to run minikube 
cluster so i cannot run the minikube service in detached mode , so instead i used a time limit , within which i am able to run the service and then it automatically stops the 
service . After this build status is sent to the gmail account ._

