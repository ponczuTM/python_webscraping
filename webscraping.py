import requests
from bs4 import BeautifulSoup
import re
import os

def repair_title(filename):
    return re.sub(r"[|%*?<>#]","",filename)

response = requests.get("https://www.kantor.pl/kursy-walut")
response.encoding = 'UTF-8'

if response.status_code == 200:

    html_content = response.text
    #print(html_content)

    page = BeautifulSoup(html_content, 'html.parser')

    if page.title:
        title = page.title.string.strip()
        title = repair_title(title)
    else:
        title = "no_title"

    filename = f"pages/{title}.html"

    directory = "pages"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # print(filename)

    with open (filename, "w", encoding="UTF-8") as file:
        file.write(html_content)

    print(f"HTML SAVED IN: {filename}")
else:
    print("CONNECTION PROBLEM")

## ASCII  A - 65
## UNICODE: UTF-8, UTF-16
## Base 64

with open ("pages/Aktualne kursy walut - kurs NBP - Kantor.pl.html", "r", encoding="UTF-8") as file:
    content = file.read()

page = BeautifulSoup(content, "html.parser")

def get_price(currency):
    buy = page.find("span", id=f"buy_{currency}").text.strip()
    sell = page.find("span", id=f"sell_{currency}").text.strip()
    return buy, sell

currencies = ["USD", "JPY", "EUR"]

get_price("USD")

for currency in currencies:
    buy, sell = get_price(currency)
    buy = buy.replace(",",".")
    sell = sell.replace(",",".")
    avg = round( (float(buy)+float(sell))/2, 2)
    print(f"{currency}:  buy for: {buy} PLN,  sell: {sell} PLN,  avg: {avg} PLN")