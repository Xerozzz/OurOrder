# OurOrder
Prerequisites:
- Docker
- Python (3.8+ recommended)
- Lightsailctl

Note: If you don't have lightsailctl, then you will need to deploy it as a container with different steps from below, or not use containers.

Deployment Steps:
1. Setup a virtualenv and run `pip install -r requirements.txt`
2. Set .env variables under `.env_sample` and rename it to `.env`
3. Run `docker build -t flask-docker .`
4. Run `docker run -p 5000:5000 flask-docker`, you can also run `flask run` first to confirm it is working 
5. Run `aws lightsail push-container-image --service-name flask-ourorder --label flask-docker --image flask-docker`
6. Edit `containers.json.sample` with the image name you retrieved in the previous command and replace `<IMAGE NAME>`
7. Run `aws lightsail create-container-service-deployment --service-name flask-ourorder --containers file://containers.json --public-endpoint file://public-endpoint.json`
8. Run `aws lightsail get-container-services --service-name flask-ourorder`


Note: To delete youri mage, run `aws lightsail delete-container-service --service-name flask-ourorder`

## Features
- ~~Consolidating of orders~~
- ~~Session ID to sync up orders from multiple devices~~
- ~~Cache to auto delete, preventing old data from being saved~~
- ~~Add price field~~
- ~~Containerize Application~~
- ~~Remarks section for customizing order or other notes~~
- Polish up CSS and styles
- ~~Allow export to Google Sheet or excel for storing purposes~~
- Adding menus for popular stores