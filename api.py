import requests
import json
from tabulate import tabulate
import time
import os
import keyboard

#pip install json

# url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"

urls = {
    "BTC": "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR,PLN",
    "ETH": "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,JPY,EUR,PLN",
    "BNB": "https://min-api.cryptocompare.com/data/price?fsym=BNB&tsyms=USD,JPY,EUR,PLN",
}

while True:
    os.system("cls")
    if(keyboard.is_pressed("esc")):
        break

    for crypto, url in urls.items():
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # data = json.dumps(data, indent = 4)
            table_data =[(currency, value) for currency, value in data.items()]
            print(f"\n-- {crypto} --")
            print( tabulate(table_data, headers=["currency", "value"], tablefmt="pretty") )
        else:
            print("CONNECTION PROBLEM")

    time.sleep(1)