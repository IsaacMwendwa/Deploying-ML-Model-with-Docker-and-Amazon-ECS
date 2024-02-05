# Deploying Productive Employment ML Model with Docker and Amazon ECS

## Current App Link: https://wage-employment-prediction.herokuapp.com/ (Outdated, new link to be posted soon)

## Introduction
This project is aimed at providing actionable insights to support SDG Number 8, by allowing users/stakeholders to do a Predictive Analysis of Productive Employment in Kenya based on Economic Growth. The project uses machine learning algorithms for the regression problem: Given the economic growth metrics (Contribution to GDP, Growth by GDP) according to Industry, predict the number of people in non-productive employment (working poor) and the total number in employment; per Industry.

## Table of Contents
* [Build_Tools](#Build_Tools)
* [Pre-requisites](#Pre-requisites)
* [Installation](#Installation)
* [Contributions](#Contributions)
* [Bug / Feature Request](#Bug--Feature-Request)
* [Authors](#Authors)

## Build_Tools
* [Python 3.6.9](https://www.python.org/) - The programming language used.
* [SciKit Learn](https://scikit-learn.org/stable/) - The machine learning library used.


## Pre-requisites
1. Anaconda from [Anaconda Organization](https://www.anaconda.com/) Installed on Local System
2. Model files from earlier project: https://github.com/IsaacMwendwa/productive-employment-prediction
3. Docker Desktop Installed with WSL 2 Integration (Ubuntu 20.04)

## Installation
1. Create a directory called "Deployment" in your system, and download/clone this repo to the folder \
   Fire up an Anaconda Prompt or terminal, and ```cd``` to the directory
3. Create a Python virtual environment using conda. Specify the Python version == 3.6.9: \
   ```conda create -n productive_employment_prediction python=3.6.9 anaconda```
4. Activate conda environment \
   ```conda activate productive_employment_prediction```
3. Install requirements as follows: \
	```pip install -r requirements.txt```
10. To execute the application, run the following command in the terminal: 
    ```Flask run```
12. The command will fire up the Flask server
13. Wait to be provided with a link on the terminal, which you can then paste in your browser to access the application
14. Locate the test file Wage_Employment_and_GDP_2018.csv in the resulting home page, select the test file upload it to get predictions
15. The predictions will then be displayed shortly thereafter

Container Creation with Docker

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
If you find a bug (the website couldn't handle the query and/or gave undesired results), kindly open an issue [here](https://github.com/IsaacMwendwa/productive-employment-prediction/issues/new) by including your search query and the expected result.

If you'd like to request a new function, feel free to do so by opening an issue [here](https://github.com/IsaacMwendwa/productive-employment-prediction/issues/new). Please include sample queries and their corresponding results.


## Authors

* **[Isaac Mwendwa](https://github.com/IsaacMwendwa)**
    
[![github follow](https://img.shields.io/github/followers/IsaacMwendwa?label=Follow_on_GitHub)](https://github.com/IsaacMwendwa)


See also the list of [Contributors](https://github.com/IsaacMwendwa/productive-employment-prediction/contributors) who participated in this project.


