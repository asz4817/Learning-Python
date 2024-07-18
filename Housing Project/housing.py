import pandas as pd
from selenium import webdriver 
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time


cService = webdriver.ChromeService(executable_path='/Users/amandazhang/Downloads/chromedriver-mac-x64/chromedriver')
driver = webdriver.Chrome(service = cService)

driver.get("https://housing.offcampus.utexas.edu/listing")


# button = driver.find_element(By.CSS_SELECTOR, 'button.btn btn-success understand')
# button.click()

#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn btn-success understand'))).click()

soup = BeautifulSoup(driver.page_source, 'lxml')

perPerson = driver.find_element('id', "perUnitLabel")
perPerson.click()

westCampus = driver.find_element('id', "neighbor-146")
westCampus.click()


apartments = driver.find_elements(By.CSS_SELECTOR, "p.ellipsis")

for i in apartments:
    button = i.find_element(By.CSS_SELECTOR, "a")
    print(button.get_attribute("innerHTML"))
    i.click()
    print(driver.page_source)
    