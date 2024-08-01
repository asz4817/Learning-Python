import pandas as pd
from selenium import webdriver 
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import StringIO
from requests_html import HTMLSession
import time



cService = webdriver.ChromeService(executable_path='/Users/amandazhang/Downloads/chromedriver-mac-x64/chromedriver')
driver = webdriver.Chrome(service = cService)


driver.get("https://housing.offcampus.utexas.edu/listing")

#I UNDERSTAND BUTTON :(
#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn btn-success understand'))).click()

# #Switch to Price Per Person
# perPerson = driver.find_element('id', "perUnitLabel")
# perPerson.click()

# #Only West Campus
# westCampus = driver.find_element('id', "neighbor-146")
# westCampus.click()

# #Load More Button
# for _ in range(3):
#     try:
#         loadMoreButton = driver.find_element(By.XPATH, "//button[@aria-label='load more button']")
#         #loadMoreButton = driver.find_element(By.CSS_SELECTOR, "button.btn my-3 btn-success btn-block")
#         loadMoreButton.click()
#         time.sleep(5)
#     except Exception as e:
#         print (e)
#         break


apartments = driver.find_element(By.CSS_SELECTOR, "div.listViewSection").find_elements(By.CSS_SELECTOR, "div.c-list")
names = driver.find_elements(By.XPATH, f"//p[contains(@class, 'ellipsis')]/a")

for i in range(len(names)):
    names[i] = names[i].get_attribute('innerHTML')
    apartments[i]= apartments[i].get_attribute("data-property-id")

print("Apartments: ", len(apartments))
print("Names: ", len(names))

data={}
try:
    for i, apartment in enumerate(apartments):
        id = apartment
        print("ID: ", id)
        driver.get(f"https://housing.offcampus.utexas.edu/listing?property={id}")

        name = names[i]
        print("Name: ", name)
        data[id] = [name]

        #PROPERTY HIGHLIGHTS
        #highlights = soup.find("div",  class_="popupDesc hasReadMore")
        categories = driver.find_elements(By.CSS_SELECTOR, ".col-md-4.col-lg-3")
        print("Found categories:", len(categories))
        propertyHighlights = []
        for c in categories:
            t = c.find_elements(By.CSS_SELECTOR, "p")
            print("LENGTH:", len(t))
            for i in t:
                text = driver.execute_script("return arguments[0].innerText;", i)
                if text != "None" and "Call" not in text:
                    propertyHighlights.append(text)
        data[id].append(propertyHighlights)
        print("PROPERTY HIGHLIGHTS: ", propertyHighlights)
        print()


        #AMENITIES
        # amenities = soup.find_element(By.XPATH, "//div[@class='popupSection row-extra']/div[@class='popupDesc']")
        amenities = driver.find_element(By.XPATH, "//div[@class='popupSection row-extra']/div[@class='popupDesc']").find_elements(By.CLASS_NAME, "row")
        propertyAmenities = []
        for a in amenities:
            x = a.find_elements(By.CSS_SELECTOR, "p")
            for i in x:
                if i.text != "Included":
                    propertyAmenities.append(i.text)
                    print(i.text)
        data[id].append(propertyAmenities)
        print("Amenities: ", propertyAmenities)
        print()

        #RENT INFO
        table = driver.find_element(By.CSS_SELECTOR, 'table')
        table_html = table.get_attribute('outerHTML')
        df = pd.read_html(table_html)[0]
        # df = df.iloc[:, 1:4]
        print(df)
        data[id].append(df)
except Exception as e:
    print("ERROR")
    print(e)
finally:
    print("DATA: ", data)
    df = pd.DataFrame.from_dict(data,  orient='index')
    df.to_csv('out.csv')