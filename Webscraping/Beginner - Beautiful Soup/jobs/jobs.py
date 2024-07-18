import requests
from bs4 import BeautifulSoup
import pandas as pd


html_text = requests.get("https://realpython.github.io/fake-jobs/").text
soup = BeautifulSoup(html_text, 'lxml')

#all jobs
results = soup.find(id = "ResultsContainer")
jobs = results.find_all("div", class_="card-content")

#Jobs with python in the title
python_jobs = [a.parent.parent.parent for a in results.find_all("h2", string=lambda text: "python" in text.lower())]

data = []
#Listing the jobs
for job in jobs:
    title = job.find("h2", class_="title").text.strip()
    company = job.find("h3", class_="company").text.strip()
    location = job.find("p", class_="location").text.strip()
    
    link = requests.get(job.find("footer").find("a").find_next()['href']).text
    info = BeautifulSoup(link, 'lxml')
    description = info.find("div", class_="box").find("p").text.strip()


    data.append([title, company, location, description])

df = pd.DataFrame(data, columns = ["Title", "Company", "Location", "Description"])
    
df.to_csv("jobs.csv")


