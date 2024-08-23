from datetime import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def plot_data(filename, ax):
    prices = []
    dates = []

    with open(filename, "r") as file:
        for line in file:
            price, date = line.split(", ")
            prices.append(float(price.replace("$", "")))
            dates.append(datetime.strptime(date.strip(), "%d/%m/%Y %H:%M:%S"))

    ax.clear()
    ax.plot(dates, prices, marker="o", linestyle="--", color="#c70ad1")
    ax.set_title(f"price for {filename}")
    ax.set_xlabel("Date")
    ax.set_ylabel("prices ($)")
    ax.grid(True)
    ax.tick_params(axis="x", rotation=30)
    plt.tight_layout()
    fig.subplots_adjust(top=0.8)
    plt.show()


directory = "data"
files = [f for f in os.listdir(directory) if f.endswith(".txt")]
#  0      1     2
# page1 page2 page3
if files:
    fig, ax = plt.subplots(figsize=(10,5)) #axis
    buttons = []
    button_axes = []
    
    for i, file in enumerate(files):
        button_axes.append(fig.add_axes([0.1*i+0.1,0.85,0.08,0.1]))


    for i, file in enumerate(files):
        button = Button(button_axes[i], file)
        button.on_clicked(lambda event, f=file: plot_data(os.path.join(directory, f), ax))
        buttons.append(button)
    plt.show()

else:
    print("No files found")