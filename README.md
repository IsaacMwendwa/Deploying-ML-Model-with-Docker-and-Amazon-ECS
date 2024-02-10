# Deploying Productive Employment ML Models with Docker and Amazon ECS

## Current App Link: [Productive Employment Prediction Application Running on Amazon ECS](http://18.220.82.49:5000/)
![image](https://github.com/IsaacMwendwa/Deploying-ML-Model-with-Docker-and-Amazon-ECS/assets/51324520/5bb17f7f-fa35-4e85-bb3d-200aebaff12a)
![image](https://github.com/IsaacMwendwa/Deploying-ML-Model-with-Docker-and-Amazon-ECS/assets/51324520/d059f8b9-a141-49f7-a0b9-37786d61ebda)
![image](https://github.com/IsaacMwendwa/Deploying-ML-Model-with-Docker-and-Amazon-ECS/assets/51324520/054ac339-3a4c-4ce8-b0d9-751fb2402c4d)




## Introduction
This project is aimed at providing actionable insights to support SDG Number 8, by allowing users/stakeholders to do a Predictive Analysis of Productive Employment in Kenya based on Economic Growth. The project uses machine learning algorithms for the regression problem: <b>Given the economic growth metrics (Contribution to GDP, Growth by GDP) according to Industry, predict the number of people in non-productive employment (working poor) and the total number in employment; per Industry</b>. The two models are deployed using Docker and Amazon EC2 for accessibility of the application

## Table of Contents
* [Build Tools](#Build-Tools)
* [Pre-requisites](#Pre-requisites)
* [Installation](#Installation)
* [Container Creation with Docker](#Container-Creation-with-Docker)
* [Push to Docker Hub](#Push-to-Docker-Hub)
* [Deploy on Amazon ECS](#Deploy-on-Amazon-ECS)
* [Contributions](#Contributions)
* [Bug / Feature Request](#Bug--Feature-Request)
* [Authors](#Authors)

## Build Tools
* [Python 3.6.9](https://www.python.org/) - The programming language used.
* [SciKit Learn](https://scikit-learn.org/stable/) - The machine learning library used.
* Docker & Docker Hub
* Amazon Elastic Container Service (ECS)


## Pre-requisites
1. Anaconda from [Anaconda Organization](https://www.anaconda.com/) Installed on Local System
2. Model files from earlier project: https://github.com/IsaacMwendwa/productive-employment-prediction
3. Docker Desktop Installed with WSL 2 Integration (Ubuntu 20.04)
4. AWS Account (AWS Management Console)

## Installation
1. Create a directory called "Deployment" in your system, and download/clone this repo to the folder \
   Fire up an Anaconda Prompt or terminal, and ```cd``` to the directory
2. Create a Python virtual environment using conda. Specify the Python version == 3.6.9: \
   ```conda create -n productive_employment_prediction python=3.6.9 anaconda```
3. Activate conda environment \
   ```conda activate productive_employment_prediction```
4. Install requirements as follows: \
	```pip install -r requirements.txt```
5. To execute the application, run the following command in the terminal: 
    ```Flask run```
6. The command will fire up the Flask server
7. Wait to be provided with a link on the terminal, which you can then paste in your browser to access the application
8. Locate the test file Wage_Employment_and_GDP_2018.csv in the resulting home page, select the test file upload it to get predictions
9. The predictions will then be displayed shortly thereafter
10. Now that we have tested the application is working in our local setup, let's move to containerization with Docker

## Container Creation with Docker
1. Create empty file in same dir --> Dockerfile, put the following commands:
	```
	FROM python:3.6.9
	EXPOSE 5000
	# 
	WORKDIR /Deployment
	# 
	COPY . .
	# 
	RUN pip install --no-cache-dir --upgrade -r /Deployment/requirements.txt 
	#
	CMD ["flask", "run", "--host", "0.0.0.0"]
	```
2. Build image by: \
    ``` docker build -t productive-employment-prediction .```
    * The command gives below output:
    * ![image](https://github.com/IsaacMwendwa/Deploying-ML-Model-with-Docker-and-Amazon-ECS/assets/51324520/fdf73a44-e1f0-4a9a-a255-f6b239afc280)
3. Create container by: \
   ```docker run --name productive-employment-prediction -d -p 5000:5000 productive-employment-prediction```
4. View container by: ```docker container ls```; or all running by: ```docker container ls -a```
5. View logs (same as in Docker Desktop logs section): \
  ```docker logs productive-employment-prediction```
	* Output of above commands:
	* ![image](https://github.com/IsaacMwendwa/Deploying-ML-Model-with-Docker-and-Amazon-ECS/assets/51324520/f7aa9cad-4059-4fab-a1c7-3d0474f2a652)
6. The address in logs is for accessing the app when in the Linux machine hosting container
7. Thus, to access the app, we need the IP Address of the Linux machine running the container
8. Gotten by 2 ways:
	(a) ipconfig --> Look for IPv4 Address of Ethernet Adapter (WSL)
	(b) Check for 5000:5000 (http://localhost:5000) in Docker Desktop
9. Open link in terminal to view the app

## Push to Docker Hub
1. Ensure you have created an account in Docker Hub’s official site, and create a repository to store the image
2. Then get back to the command line interface
3. Start by confirming your created image is listed, and note the Tag: \
  ```docker images```
4. Login to your Docker Hub account: ```docker login```
5. Create a tag for the DH repository image:
	* Format: docker tag local-image:tagname dockerhubname/local-image:tagname
	* This case: \
	```docker tag productive-employment-prediction:latest isaac1017/productive-employment-prediction:latest```
	* Confirm Tag Creation: ```docker images```
6. Push your image to the Docker Hub: ```docker push dockerhubname/reponame:tagname```
	* This case: ```docker push isaac1017/productive-employment-prediction:latest```
7. Go to Docker Hub, and confirm creation of the repo

## Deploy on Amazon ECS
* Next we deploy the Productive Employment Prediction app on AWS ECS from DH Registry
* The steps are as follows:
1. Log in to AWS Management Console
   * Search for ECS (Elastic Container Service)
2. Create Cluster
   * Cluster Configuration: Input your Cluster name 
   * Infrastructure: AWS Fargate, Amazon EC2, External instances (Choose Fargate)
   * Click Create Cluster
3. Create New Task Definition (with AWS Fargate)
   * Task Definition COnfiguration: Input task definition family name
   * Infrastructure Requirements:
   	* Launch Type: AWS Fargate
   	* OS/Architecture: Linux/X86_64
   	* Task size (for reserving resources for task): CPU (.25 vCPU), Memory (1 GB)
   	* Container: Name, Image URI(Input your container name from Docker Hub Repository), Essential container (Yes)
   	* Port Mappings: Container Port: 5000, Protocol: TCP, Port name, App Protocol: HTTP
	* Create Task Definition
 	* After successful creation of task definition, click Deploy - Run Task; which will setup the task definition environment 
 4. Run Task - downloads the image and deploys it in a container
    * Environment: Choose existing created cluster
    * Compute options: Click Launch type (to launch tasks directly without use of a capacity provider strategy)
    * Launch Type: FARGATE; Platform: LATEST
    * Deployment Configuration
  	* Application Type: Task (standalone task, not service)
    * Networking
     	* Select at least 1 subnet (leave the 3 default subnets)
  	* In Security Group, Create a new Security group, give it a name and description
  		* Define the inbound rules for the Security Group as follows: Type: Custom TCP Proctocol: TCP, Port Range: 5000, Source: Anywhere
  	* Turn on Public IP to the task's elastic network interface
5. Click Create - will launch the task
   *If the task's last status moves from "Provisioning" to "Running", then the task is successfully deployed
   * The running task will be accessible with the public IP address provided, coupled with port i.e ```http://public_ip_addr:port``` in your browser
   * The Productive Employment Prediction Models are now deployed on Amazon ECS: [Deployed Application](http://18.220.82.49:5000/)
   * <img width="946" alt="image" src="https://github.com/IsaacMwendwa/Deploying-ML-Model-with-Docker-and-Amazon-ECS/assets/51324520/9068eb72-36da-48b4-8a19-bc840d9b5a34">
   * <img width="937" alt="image" src="https://github.com/IsaacMwendwa/Deploying-ML-Model-with-Docker-and-Amazon-ECS/assets/51324520/164b69e6-41f3-438b-a200-f4647ad4a005">




## Contributions
Contributions are welcome using pull requests. To contribute, follow these steps:
1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`
3. Make your changes to relevant file(s)
4. Check status of your commits: `git status`
6. Add and commit file(s) to the repo using:
    `git add <file(s)>`
    `git commit -m "<message>"`
8. Push repo to Github: `git push origin <branch_name`
9. Create the pull request. See the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Bug / Feature Request
If you find a bug (the website couldn't handle the query and/or gave undesired results), kindly open an issue [here](https://github.com/IsaacMwendwa/Deploying-ML-Model-with-Docker-and-Amazon-ECS/issues/new) by including your search query and the expected result.

If you'd like to request a new function, feel free to do so by opening an issue [here](https://github.com/IsaacMwendwa/Deploying-ML-Model-with-Docker-and-Amazon-ECS/issues/new). Please include sample queries and their corresponding results.


## Authors

* **[Isaac Mwendwa](https://github.com/IsaacMwendwa)**
    
[![github follow](https://img.shields.io/github/followers/IsaacMwendwa?label=Follow_on_GitHub)](https://github.com/IsaacMwendwa)


See also the list of [Contributors](https://github.com/IsaacMwendwa/Deploying-ML-Model-with-Docker-and-Amazon-ECS/contributors) who participated in this project.


