from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from tasks import scrape_data
import uuid
import csv
from pathlib import Path
from selenium.webdriver.common.action_chains import ActionChains
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

class NemligScraper():
    def __init__(self):
        self.file_name = self.create_file()
        opts = Options()
        opts.headless = True
        profile = webdriver.FirefoxProfile()

        profile.set_preference("dom.webnotifications.enabled", False)
        self.browser = webdriver.Firefox(firefox_profile=profile, options=opts, executable_path=f'{BASE_DIR}/geckodriver.exe')
        self.nemlig_list()
        # self.scrape_urls()
        # self.get_urls()
        self.browser.close()

    def nemlig_list(self):

        with open('scraped_urls0-1500.txt', 'r') as file:
            urls = file.readlines()
            with open(f'all_scraped_data/{self.file_name}.csv', 'a+', newline='') as file:
                writer = csv.writer(file)
                click = True
                for i, url in enumerate(urls):
                    print('-----------------------------', i, url)
                    self.browser.get(url)
                    if click:
                        self.browser.find_element_by_class_name('coi-banner__accept').click()
                        click = False
                    time.sleep(1)
                    breadcrumb = ''
                    product_name = ''
                    weight = ''

                    brand = ''
                    egnet_til = ''
                    emballage = ''
                    farve = ''
                    klasse = ''
                    land = ''
                    markininger = ''
                    oprindes = ''
                    sort = ''
                    storelse = ''
                    type_of_product = ''

                    product_detail_labels = ''
                    base_price = ''
                    discounted_price = ''
                    product_attributes = ''
                    product_detail = ''
                    url = ''

                    try:
                        breadcrumb = self.browser.find_element_by_tag_name('breadcrumb')
                        breadcrumb = [i.text for i in breadcrumb.find_elements_by_tag_name('li')]
                    except:
                        breadcrumb = []
                    try:
                        product_name = self.browser.find_element_by_class_name('product-detail__header').text
                    except:
                        product_name=''
                    try:
                        weight = self.browser.find_element_by_class_name('product-detail__subheader').text
                    except:
                        product_name_subheader = ''
                    try:
                        labels = [i.get_attribute('alt') for i in self.browser.find_elements_by_class_name('labels__item-image')]

                    except:
                        labels = []
                    try:
                        base_price = self.browser.find_element_by_class_name('pricecontainer__base-price').text
                        base_price = base_price[:-3]+'.'+base_price[-2:]
                    except:
                        base_price = ''
                    try:
                        discounted_price = self.browser.find_element_by_class_name('pricecontainer__campaign-price').text
                        discounted_price = discounted_price[:-3]+'.'+discounted_price[-2:]
                    except:
                        discounted_price = ''
                    try:
                        product_attributes = self.browser.find_elements_by_class_name('product-detail__attribute')
                        
                        for i in range(len(product_attributes)):
                            key = product_attributes[i].find_element_by_class_name('product-detail__attribute-key').text
                            values = product_attributes[i].find_elements_by_class_name('product-detail__attribute-value')
                            value = ' '.join([str(elem.text) for elem in values])
                            if key.startswith('Brand'):
                                brand = value
                            elif key.startswith('Egnet'):
                                egnet_til = value
                            elif key.startswith('Emballage'):
                                emballage = value
                            elif key.startswith('Farve'):
                                farve = value
                            elif key.startswith('Klas'):
                                klasse = value
                            elif key.startswith('Land'):
                                land = value
                            elif key.startswith('Mærk'):
                                markininger = value
                            elif key.startswith('Opri'):
                                oprindes = value
                            elif key.startswith('Sort'):
                                sort = value
                            elif key.startswith('Stø'):
                                storelse = value
                            elif key.startswith('Type'):
                                type_of_product = value

                    except Exception as e:
                        pass
                    try:
                        self.browser.execute_script("window.scrollTo(0, window.scrollY + 500)") 
                        time.sleep(1)
                        self.browser.save_screenshot('detail.png')
                        product_detail = self.browser.find_element_by_class_name('product-detail__description-text').text
                        time.sleep(1)
                    except Exception as e:
                        product_detail = ''
                    labels = ','.join([str(elem) for elem in labels])
                    breadcrumb = ' > '.join([str(elem) for elem in breadcrumb])
                    url = self.browser.current_url

                    data = [
                        breadcrumb, product_name, weight, 
                        labels, base_price, discounted_price, brand, egnet_til, 
                        emballage, farve, klasse, land, markininger, 
                        oprindes, sort, storelse, type_of_product, product_detail, url
                    ]
                    if len(product_name) != 0:
                        writer.writerow(data)

    def create_file(self):
        filename = 'nemlig'+uuid.uuid4().hex
        # header = [
        #     'breadcrumb','product name','weight', 'labels',
        #     'base price', 'discounted price', 'attributes', 'product detail text', 'url',
        # ]
        header = [
            'Breadcrumb','Product Name','Weight', 'Labels',
            'Base price', 'Discounted price', 'Brand', 'Egnet til', 'Emballage', 'Farve',
            'Klasse', 'Land', 'Mærkninger', 'Oprindelsesland', 'Sort', 'Størelse',
            'Type','Product Detail text', 'URL',
        ]
        new_file = open(f'all_scraped_data/{filename}.csv', 'w')
        writer = csv.writer(new_file)
        writer.writerow(header)
        new_file.close()
        return filename

    def scrape_urls(self):
        with open('urls0-300.txt', 'r') as file:
            lines = file.readlines()
            new_links = set()
            print('--links without set', len(lines))
            for l in lines:
                new_links.add(l)
            print(len(new_links))
            with open('scraped_urls0-300.txt', 'a+') as f:
                for i, link in enumerate(new_links):
                    print(i, link)
                    self.browser.get(link)
                    time.sleep(1)
                    try:
                        self.browser.find_element_by_class_name('coi-banner__accept').click()
                    except:
                        pass
                    self.browser.save_screenshot('last.png')
                    time.sleep(3)
                    l = self.browser.find_elements_by_tag_name('productlist-item')
                    spots = self.browser.find_elements_by_class_name('productlistshowallspot')
                    one_row_wrap = self.browser.find_elements_by_class_name('productlist-onerow__item-wrap')
                    new_file = open('scraped_urls.txt', 'w')
                    new_file.close()
                    for i in range(len(one_row_wrap)):
                        time.sleep(2)
                        self.browser.save_screenshot('aaaa.png')
                        self.browser.execute_script("arguments[0].scrollIntoView();", one_row_wrap[i])
                        time.sleep(4)
                        for i in one_row_wrap[i].find_elements_by_tag_name('productlist-item'):
                            try:
                                a_tag = i.find_element_by_tag_name('a').get_attribute('href')
                                print(a_tag)
                                f.writelines(a_tag+'\n')
                            except:
                                pass
                    for i in range(len(spots)):
                        self.browser.execute_script("arguments[0].scrollIntoView();", spots[i])
                        time.sleep(4)
                        for i in spots[i].find_elements_by_tag_name('productlist-item'):
                            try:
                                a_tag = i.find_element_by_tag_name('a').get_attribute('href')
                                print(a_tag)
                                f.writelines(a_tag+'\n')
                            except:
                                pass

NemligScraper()




