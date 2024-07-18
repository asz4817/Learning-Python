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

driver.get("https://realpython.github.io/fake-jobs/")
page = driver.page_source
original_window = driver.current_window_handle

soup = BeautifulSoup(page, 'lxml')

results = soup.find(id = "ResultsContainer")
jobs = results.find_all("div", class_="card-content")

#Jobs with python in the title
python_jobs = [a.parent.parent.parent for a in results.find_all("h2", string=lambda text: "python" in text.lower())]


buttons = driver.find_elements(By.LINK_TEXT, "Apply")


data = []
#Listing the jobs
for i, job in enumerate(jobs):
    title = job.find("h2", class_="title").text.strip()
    company = job.find("h3", class_="company").text.strip()
    location = job.find("p", class_="location").text.strip()
    
    #link = requests.get(job.find("footer").find("a").find_next()['href']).text
    #print(buttons[i].get_attribute("outerHTML"))

    buttons[i].click()
    new_window = driver.window_handles[1]
    driver.switch_to.window(new_window)
    info = BeautifulSoup(driver.page_source, 'lxml')
    assert info != soup
    description = info.find("div", class_="box").find("p").text.strip()

    data.append([title, company, location, description])
    driver.close()
    driver.switch_to.window(original_window)

df = pd.DataFrame(data, columns = ["Title", "Company", "Location", "Description"])

print(df)

df.to_csv("test.csv")


driver.close()




