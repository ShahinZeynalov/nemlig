

# README #

# Scrape Flta.com with Selenium & Celery &RabbitMQ & BeautifulSoup #

### https://www.flta.org/IndMemberDirectory?&tab=1 ###

First you need to clone this repo to your local computer.
```sh
$ git clone https://github.com/ShahinZeynalov/scrape_flta_with_selenium_celery_rabbitmq
$ cd scrape_flta_with_selenium_celery_rabbitmq/
```

### --- Download requirements ###
After successfuly installed project you need to download requirements.
```sh
$ pip install -r requirements.txt
```
Or download via [virtualenv](https://linuxize.com/post/how-to-create-python-virtual-environments-on-ubuntu-18-04/)



### --- Build Docker ###
After successfuly download requirements you need to Build docker bellow command:
```sh
$ docker-compose up -d --build
```
For more info about docker visit to [docker hub](https://hub.docker.com/)

### --- Run celery ###
After successfuly build docker you need to run celery with below command:
```sh
$ celery -A tasks worker --loglevel=INFO --autoscale=AUTOSCALE
```
For more info go to offical documentation.

### --- Run scaper ###
```sh
$ python scrape.py
```

----------------------------------------------------------------------------------------------------------------------------------------------------------------

### --- Used modules & Apps ###
1. Selenium: [selenium offical](https://www.selenium.dev/selenium/docs/api/py/)
2. Celery: [celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html)
2. BeautifulSoup: [bs4](https://pypi.org/project/beautifulsoup4/)