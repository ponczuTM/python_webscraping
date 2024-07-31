import requests

response = requests.get("https://google.com")

if response.status_code == 200:
    print("CONNECTION OK")
else:
    print("CONNECTION PROBLEM")