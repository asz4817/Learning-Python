import requests
from bs4 import BeautifulSoup
import pandas as pd

#html_text = requests.get("")




html_text = requests.get("https://www.scrapethissite.com/pages/simple/").text
soup = BeautifulSoup(html_text, 'lxml')
countries = soup.find("div", id = "page").find("div", class_="container").find_all("div", class_ = "row")[3:]

data = []
for country in countries:
    name = country.find("h3", class_="country-name").text.strip()
    capital = country.find("span", class_="country-capital").text.strip()
    population = int(country.find("span", class_="country-population").text.strip())
    area = float(country.find("span", class_="country-area").text.strip())
    data.append([name, capital, population, area])

df = pd.DataFrame(data, columns=["Country", "Capital", "Population", "Area (km^2)"])
print(df)

df.to_csv("countries.csv")
