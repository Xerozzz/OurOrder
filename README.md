# OurOrder
A group order application that allows multiple people to easily compile and consolidate individual orders at a restaurant or eatery.

Uses a Redis cache and session ID system to sync up orders from multiple devices and individuals easily. Allows input of information like order name, price, any special requirements etc. Also allows you to export everyones orders into an Excel sheet for storage or saving.

Orders are cleared after 1800 seconds.

Application runs on Python Flask and can be containerised to run on Amazon LightSail Containers or Docker, or deployed as an Elastic Beanstalk application.

## Problem
Sometimes when we go to restaurants, you are required to make your order at the counter. 

Usually one person is elected to go make that order and if the group is big or has multiple iems, it can be hard to remember them all

Furthermore, when it comes time to split the bill, we may forget who ordered what

OurOrder solves that problem by allowing people to easily access and consolidate orders

## Principle
Simple to develop, easy to maintain and convenient to use

## Prerequisites:
- Python (3.8+ recommended)
- AWS CLI (and configured credentials using `aws configure`)
### Deployment Requirements
- Docker and Lightsailctl
<br>OR
- EB CLI (Elastic Beanstalk CLI)

## Deployment Steps:

### Setup
1. Setup a virtualenv and run `pip install -r requirements.txt`
2. Set .env variables under `.env_sample` and rename it to `.env`

### Testing and Linting
- `autopep8 --recursive --in-place --aggressive --aggressive app.py`
- `autopep8 --recursive --in-place --aggressive --aggressive functions.py`
- `pylint *.py`
- `pytest` (3 tests will fail if you do not have a local running Redis instance)

### As an Elastic Beanstalk Application using GitHub
3. Run `eb init` in the root directory
4. Run `eb create` to create your EB environment
5. Run `eb deploy` to deploy your application (also run this command when new changes are pushed to the repo)

Other commands:

- `eb status` - Used to check status of your deployment  
- `eb open` - Opens your application URL
- `eb console` - Opens your application in the AWS Console

### As a AWS LightSail or Docker Container (Old method)
Note: All files are under "Lightsail Containers Scripts" Folder. Edit the commands as necessary or drag the files into the main directory.

3. Run `docker build -t flask-docker .`
4. Run `docker run -p 5000:5000 flask-docker`, you can also run `flask run` first to confirm it is working 
5. Run `aws lightsail push-container-image --service-name flask-ourorder --label flask-docker --image flask-docker`
6. Edit `containers.json.sample` with the image name you retrieved in the previous command and replace `<IMAGE NAME>`
7. Run `aws lightsail create-container-service-deployment --service-name flask-ourorder --containers file://containers.json --public-endpoint file://public-endpoint.json`
8. Run `aws lightsail get-container-services --service-name flask-ourorder`

Note: To delete your image, run `aws lightsail delete-container-service --service-name flask-ourorder`

## Features
### Open Bugs

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
- Creating continuous documentation and deployment on Elastic Beanstalk

### Future/Developing
- Using Selenium to do end-to-end testing
- Adding menus for popular stores
- Adding Icons for fun and personalisation
