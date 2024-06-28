import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []
for i in range(1, 51):
    html_text = requests.get(f"http://books.toscrape.com/catalogue/page-{i}.html").text
    soup = BeautifulSoup(html_text, 'lxml')
    books = soup.find("ol", class_ = "row").find_all("article", class_ = "product_pod")
    for book in books:
        title = book.find("img")['alt']
        rating = book.find("p")['class'][1]
        price = float(book.find("p", class_="price_color").text[2:])
        data.append([title, rating, price])

df = pd.DataFrame(data, columns= ["Title", "Rating", "Price"])
df.to_csv("books.csv")
