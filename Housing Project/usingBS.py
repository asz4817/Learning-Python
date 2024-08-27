from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import sys
import time

def help(id):
    # Create an HTML Session

    session = HTMLSession()
    # Fetch the page
    response = session.get(f"https://housing.offcampus.utexas.edu/listing?property={id}")
    time.sleep(10)
    # Render the JavaScript
    response.html.render(timeout=20)
    # Get the rendered HTML content
    html_text = response.html.html
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_text, 'lxml')

    #PROPERTY HIGHLIGHTS
    #highlights = soup.find("div",  class_="popupDesc hasReadMore")
    categories = soup.find_all("div", class_="col-md-4 col-lg-3")
    propertyHighlights = dict()
    for c in categories:
        highlights = c.find("h3").text
        propertyHighlights[highlights] = []
        t = c.find_all("p")
        for i in t:
            propertyHighlights[highlights].append(i.text)
    print("PROPERTY HIGHLIGHTS: ", propertyHighlights)
    print()


    #AMENITIES
    # amenities = soup.find_element(By.XPATH, "//div[@class='popupSection row-extra']/div[@class='popupDesc']")
    amenities = soup.select('div.popupSection.row-extra > div.popupDesc')[0].find_all("div", class_="row")
    propertyAmenities = []
    for a in amenities:
        x = a.find_all("p")
        for i in x:
            if i.text != "Included":
                propertyAmenities.append(i.text)
    print("Amenities: ", propertyAmenities)
    print()

    #RENT INFO
    table = soup.find("div", class_="table-view").find('table')
    df = pd.read_html(StringIO(str(table)))[0]
    df = df.iloc[:, 1:4]
    print(df)

    return propertyHighlights, propertyAmenities, df


# # Create an HTML Session
# session = HTMLSession()
# # Fetch the page
# response = session.get("https://housing.offcampus.utexas.edu/listing?property=72262")
# # Render the JavaScript
# response.html.render(timeout=20)
# # Get the rendered HTML content
# html_text = response.html.html
# # Parse the HTML content using BeautifulSoup
# soup = BeautifulSoup(html_text, 'lxml')

# print("BEFORE ERROR?")

# name = soup.find("div", id="detailPopup___BV_modal_body_").find("div", class_="propNamePills").find("a").text
# print("NAME: ", name)
# print()


# #PROPERTY HIGHLIGHTS
# highlights = soup.find("div",  class_="popupDesc hasReadMore")
# categories= highlights.find_all("div", class_="col-md-4 col-lg-3")
# propertyHighlights = dict()
# for c in categories:
#     name = c.find("h3").text
#     propertyHighlights[name] = []
#     t = c.find_all("p")
#     for i in t:
#         propertyHighlights[name].append(i.text)
# print("PROPERTY HIGHLIGHTS: ", propertyHighlights)

# print()
# print("IN BETWEEN")
# print()

# #AMENITIES
# # amenities = soup.find_element(By.XPATH, "//div[@class='popupSection row-extra']/div[@class='popupDesc']")
# amenities = soup.select('div.popupSection.row-extra > div.popupDesc')[0].find_all("div", class_="row")
# propertyAmenities = []
# for a in amenities:
#     x = a.find_all("p")
#     for i in x:
#         if i.text != "Included":
#             propertyAmenities.append(i.text)
# print("Amenities: ", propertyAmenities)

# print()
# print("IN BETWEEN 2")
# print()

# #RENT INFO
# table = soup.find("div", class_="table-view").find('table')

# df = pd.read_html(StringIO(str(table)))[0]
# print(df)
def main():
    pass

if __name__=="__main__":
    help()