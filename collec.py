from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
)
from openpyxl import Workbook
import time

driver = webdriver.Chrome()
workbook = Workbook()
sheet = workbook.active

sheet.append(["Links"])
links = []


def extract_links(a_tags):
    for tag in a_tags:
        link = tag.get_attribute("href")
        if not link in links:
            links.append(link)
            sheet.append([link])
            print("added")


driver.get("https://www.freecodecamp.org/news/tag/programming/")
time.sleep(2)


i = 0
# change 10 to  100
while i < 10:
    print(i)
    a_tags = driver.find_elements(by=By.CLASS_NAME, value="post-card-image-link")
    try:
        load_more = driver.find_element(by=By.ID, value="readMoreBtn")
        extract_links(a_tags=a_tags)
        load_more.click()
    except (NoSuchElementException, StaleElementReferenceException) as e:
        print("No load more btn")
    i += 1


workbook.save("sheet.xlsx")
