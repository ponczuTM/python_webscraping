import requests
from bs4 import BeautifulSoup
import re
import os
from tabulate import tabulate
import time
import tkinter as tk
from tkinter import ttk
import threading

# wątki - theards
# deamons 

# padx=2 pady=1 grid
#       2
#   1
#   

padx_for_table = 20
currencies = ["USD", "JPY", "EUR"]
labels = {}

def repair_title(filename):
    return re.sub(r"[|%*?<>#]","",filename)

def get_html():
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

        with open (filename, "w", encoding="UTF-8") as file:
            file.write(html_content)

        return filename

    else:
        print("CONNECTION PROBLEM")
        return None

## ASCII  A - 65
## UNICODE: UTF-8, UTF-16
## Base 64


def get_prices(page, currency):
    buy = page.find("span", id=f"buy_{currency}").text.strip()
    sell = page.find("span", id=f"sell_{currency}").text.strip()
    return buy, sell

def update_currencies():

    filename = get_html()

    with open (filename, "r", encoding="UTF-8") as file:
        content = file.read()

    page = BeautifulSoup(content, "html.parser")

    for currency in currencies:
        buy, sell = get_prices(page, currency)
        buy = buy.replace(",",".")
        sell = sell.replace(",",".")
        avg = round( (float(buy)+float(sell))/2, 2)

        labels[currency]["buy"].config(text=buy)
        labels[currency]["sell"].config(text=sell)
        labels[currency]["avg"].config(text=avg)
    gui.after(100, start_update_threads)

def start_update_threads():
    threading.Thread(target=update_currencies(), daemon=True).start()

gui = tk.Tk()
gui.title("CURRENCIES")
gui.geometry("600x300")

headers = tk.Label(gui, text="LIVE CURRENCY WEBSCRAPING", font=("Arial", 18))
headers.pack(pady=35)

table_frame = ttk.Frame(gui)
table_frame.pack(pady=5)

#USD", "JPY", "EUR"
ttk.Label(table_frame, text="Currency", font=("Arial", 14)).grid(row=0, column=0, padx = padx_for_table)
ttk.Label(table_frame, text="BUY (PLN)", font=("Arial", 14)).grid(row=0, column=1, padx = padx_for_table)
ttk.Label(table_frame, text="SELL (PLN)", font=("Arial", 14)).grid(row=0, column=2, padx = padx_for_table)
ttk.Label(table_frame, text="AVG (PLN)", font=("Arial", 14)).grid(row=0, column=3, padx = padx_for_table)

for i, currency in enumerate(currencies, start=1):
    ttk.Label(table_frame, text=currency, font=("Arial", 14)).grid(row=i, column=0, padx=padx_for_table)

    labels[currency] = {
        "buy": ttk.Label(table_frame, text="N/A", font=("Arial", 14)),
        "sell": ttk.Label(table_frame, text="N/A", font=("Arial", 14)),
        "avg": ttk.Label(table_frame, text="N/A", font=("Arial", 14))
    }

    labels[currency]["buy"].grid(row=i, column=1, padx=padx_for_table)
    labels[currency]["sell"].grid(row=i, column=2, padx=padx_for_table)
    labels[currency]["avg"].grid(row=i, column=3, padx=padx_for_table)


# labels[currency]["buy"]

start_update_threads()

gui.mainloop()