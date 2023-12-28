from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import time
from string import ascii_lowercase as alc
import atexit
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Chrome()
all_products = []
BASE_URL = 'URL_OF_SITE'
urls = set()
prodcut_links = set()

def get_urls ():
    driver.get(BASE_URL)
    time.sleep(5)
    categories_links = driver.find_elements(By.CLASS_NAME, 'category-link')
    for link in categories_links:
        urls.add(link.get_attribute('href'))

def scrape_product(link, category):
    driver.get(link)
    time.sleep(5)
    product = {}
    
    product["name"] = driver.find_element(By.CLASS_NAME, 'product_title').text
    try: 
        product["description"] = driver.find_element(By.ID, 'tab-description').text
    except:
        product["description"] = ''
    time.sleep(2)
    product["price"] = driver.find_element(By.CLASS_NAME, 'price').text
    product["category"] = category
    try: 
        product["image"] = driver.find_element(By.CLASS_NAME, 'zoomImg').get_attribute('src')
    except:
        product["image"] = ''
    

    # print(product)
    if product["price"] != '':
        all_products.append(product)
    print(len(all_products))

def start(url):
    category = url.split('/')[-2]    
    driver.get(url)
    time.sleep(5)
    print(category)
    try: 
        #iterate pages
        while True:
            
            # get product links
            products = driver.find_elements(By.CLASS_NAME, 'product-image-link')
            for product in products:
                prodcut_links.add(product.get_attribute('href') + ' ' + category)    
                
            # go to next page
            next = driver.find_element(By.CLASS_NAME, 'next')
            next = next.get_attribute('href')        
            driver.get(next)
            time.sleep(5)   
    except:
        print('End of pages for ' + category)
    

get_urls()

for url in urls:
    start(url)

# scrape each product
for product_link in prodcut_links:
    product = product_link.split(' ')
    scrape_product(product[0], product[1])

print(len(all_products))

with open("results.csv", "w", newline="") as outfile:
    writer = csv.DictWriter(outfile, all_products[0].keys())
    writer.writeheader()
    writer.writerows(all_products)
