import os
import re
from bs4 import BeautifulSoup
import requests
import datetime

page_title = "page"
i = 1

urls = [
    "https://www.alibaba.com/product-detail/Aikun-GX610-Gaming-Keyboard-USB-Interface_1600083959097.html?spm=a2700.galleryofferlist.topad_classic.d_image.752917ccWNvYY9",
    "https://www.alibaba.com/product-detail/Clavier-de-jeu-Lightweight-Wired-Gaming_1600142159781.html?spm=a2700.details.buy_together.3.75e14d90P09q98",
    "https://www.alibaba.com/product-detail/GX5600-4-IN-1-Gaming-Combo_1601178326490.html?spm=a2700.details.popular_products.11.a19e3691Wt19Ci"
]

def repair_title(filename):
    return re.sub(r"[|%*?<>#]","",filename)

def get_html(url):
    response = requests.get(url)
    response.encoding = 'UTF-8'

    if response.status_code == 200:

        html_content = response.text

        filename = f"alibaba/{page_title}.html"

        directory = "alibaba"
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open (filename, "w", encoding="UTF-8") as file:
            file.write(html_content)

    else:
        print("CONNECTION PROBLEM")

def extract_price(html_content):
    page = BeautifulSoup(html_content, "html.parser")
    price_items = page.find_all("div", class_="price-item")
    price_div = price_items[0].find("div", class_="price")
    if price_div:
        price_span = price_div.find("span")
        if price_span:
            return price_span.get_text(strip=True)
    return None

for url in urls:
    page_title = f"page{i}"
    i+=1
    get_html(url)


alibaba_directory = "alibaba"
data_directory = "data"

if not os.path.exists(data_directory):
    os.makedirs(data_directory)

for filename in os.listdir(alibaba_directory):
    if (filename.endswith(".html")):
        file_path = os.path.join(alibaba_directory, filename)
        with open(file_path, "r", encoding="UTF-8") as file:
            html_content = file.read()
            price = extract_price(html_content)
            if price:
                title = os.path.splitext(filename)
                data_file_path = os.path.join(data_directory, f"{title[0]}.txt")
                current_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                with open(data_file_path, "a", encoding="UTF-8") as data_file:
                    data_file.write(f"{price}, {current_date}\n")