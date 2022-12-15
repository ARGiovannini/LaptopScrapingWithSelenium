from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv

file = open("Laptops.csv", "w")
writer = csv.writer(file)
writer.writerow(["Unique ID", "Name", "Price", "Specifications", "Number of reviews"])

browser_driver = Service('/Users/alexgiovannini/Desktop/DevCC/Week 17 Selenium/chromedriver')
scraper = webdriver.Chrome(service=browser_driver)

scraper.get("https://webscraper.io/test-sites/e-commerce/static/computers/laptops")
try:
    cookies = scraper.find_element(By.CLASS_NAME, "acceptCookies")
    cookies.click()
except NoSuchElementException:
    pass

rows = []
while True:
    laptops = scraper.find_elements(By.CLASS_NAME, "col-sm-4.col-lg-4.col-md-4")
    for laptop in laptops:
        name = laptop.find_element(By.CLASS_NAME, "title").get_attribute("title")
        price = laptop.find_element(By.CLASS_NAME, "pull-right.price").text[1:]
        spec = laptop.find_element(By.CLASS_NAME, "description").text
        num_reviews = laptop.find_element(By.CLASS_NAME, "ratings").find_element(By.CLASS_NAME, "pull-right").text.split(None, 1)[0]
        rows.append({"name": name, "price": float(price), "specifications": spec, "number of reviews": int(num_reviews)})
    try:
        element = scraper.find_element(By.PARTIAL_LINK_TEXT, "›")
        element.click()
    except NoSuchElementException:
        break

sorted_rows = sorted(rows, key=lambda k:k['price'])

unique_ID = 1
for i in range(len(sorted_rows)):
    sorted_rows[i]["unique_ID"] = unique_ID
    unique_ID += 1
    writer.writerow([sorted_rows[i]["unique_ID"], sorted_rows[i]["name"], f'${sorted_rows[i]["price"]}', sorted_rows[i]["specifications"], sorted_rows[i]["number of reviews"]])