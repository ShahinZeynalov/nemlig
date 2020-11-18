from celery import Celery
from celery import shared_task
from bs4 import BeautifulSoup as bs4
import requests
from os.path import isfile
import csv
from utils import validate_data

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@shared_task
def scrape_data(link, file_name):
    detail = requests.get(link)
    soup = bs4(detail.content, 'html.parser')
    membership_level = validate_data(soup.find('div', {'id':'idMembershipLevelContainer'}))
    organization=validate_data(soup.find('div', {'id': 'idContainer2075262'}))
    first_name = validate_data(soup.find('div', {'id':'idContainer2075260'}))
    nick_name = validate_data(soup.find('div', {'id': 'idContainer2100498'}))
    last_name = validate_data(soup.find('div', {'id': 'idContainer2075261'}))
    email = validate_data(soup.find('div', {'id': 'idContainer2075259'}))
    street_address = validate_data(soup.find('div', {'id': 'idContainer2783240'}))
    city = validate_data(soup.find('div', {'id': 'idContainer2100502'}))
    state = validate_data(soup.find('div', {'id': 'idContainer2100503'}))
    zip_code = validate_data(soup.find('div', {'id': 'idContainer2783241'}))
    phone = validate_data(soup.find('div', {'id': 'idContainer2075265'}))
    office = validate_data(soup.find('div', {'id': 'idContainer2783253'}))
    job_title = validate_data(soup.find('div', {'id': 'idContainer2075270'}))


    data = [
        membership_level, organization, first_name, 
        last_name, nick_name, email, street_address, city,
        state, zip_code, phone, office, job_title
    ]

    with open(f'all_scraped_data/{file_name}.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    return 'Task Done!!!'

