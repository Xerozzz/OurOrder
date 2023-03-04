# OurOrder
A group order application that allows multiple people to easily compile and consolidate individual orders at a restaurant or eatery.

Uses a cache and session ID system to sync up orders from multiple devices and individuals easily. Allows input of information like order name, price, any special requirements etc. Also allows you to export everyones orders into an Excel sheet for storage or saving.

Orders are cleared after 1800 seconds.

Application runs on Python Flask and can be containerised to run on Amazon LightSail Containers or Docker.

## Problem
Sometimes when we go to restaurants, you are required to make your order at the counter. 

Usually one person is elected to go make that order and if the group is big or has multiple iems, it can be hard to remember them all

Furthermore, when it comes time to split the bill, we may forget who ordered what

OurOrder solves that problem by allowing people to easily access and consolidate orders

## Principle
Simple to develop, convenient to maintain and easy to use

## Prerequisites:
- Docker
- Python (3.8+ recommended)
- Lightsailctl

Note: If you don't have lightsailctl, then you will need to deploy it as a container with different steps from below, or not use containers.

## Deployment Steps:
### As a AWS LightSail or Docker Container
Note: All files are under "Lightsail Containers Scripts" Folder. Edit the commands as necessary or drag the files into the main directory.
1. Setup a virtualenv and run `pip install -r requirements.txt`
2. Set .env variables under `.env_sample` and rename it to `.env`
    <br>Optional: Run `python -m pytest -v --setup-show --cov=app --cov-report term-missing` to test the code.

3. Run `docker build -t flask-docker .`
4. Run `docker run -p 5000:5000 flask-docker`, you can also run `flask run` first to confirm it is working 
5. Run `aws lightsail push-container-image --service-name flask-ourorder --label flask-docker --image flask-docker`
6. Edit `containers.json.sample` with the image name you retrieved in the previous command and replace `<IMAGE NAME>`
7. Run `aws lightsail create-container-service-deployment --service-name flask-ourorder --containers file://containers.json --public-endpoint file://public-endpoint.json`
8. Run `aws lightsail get-container-services --service-name flask-ourorder`


Note: To delete your image, run `aws lightsail delete-container-service --service-name flask-ourorder`

### CI/CD Pipeline using CodeDeploy, LightSail and CodePipeline
1. To be added

## Features
### Bugs
- Session IDs not working on orders page if sent by 2 diff devices

### Implemented
- Consolidating of orders
- Session ID to sync up orders from multiple devices
- Cache to auto delete, preventing old data from being saved
- Add price field
- Remarks section for customizing order or other notes
- Polish up CSS and styles
- Allow export to Google Sheet or excel for storing purposes
- Functional and Unit Tests
- Deployment as Container in AWS Lightsail or Docker
- Deployment with fully CI/CD Pipeline using CodeDeploy, CodePipeline and Lightsail

### Future/Developing
- Automate full CI/CD deployment into the cloud using Terraform
- Creating a safer way to port .env into CodePipeline
- Adding menus for popular stores
- Adding Icons for fun and personalisation
- Find a way to prevent possible clashing of session IDs