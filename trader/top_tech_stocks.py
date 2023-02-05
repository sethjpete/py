import pandas as pd

df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
df = df[(df["GICS Sector"] == "Information Technology") | (df["GICS Sector"] == "Communication Services")]
symbols = df["Symbol"].tolist()

with open("TSDA/_symbols.txt", "w") as f:
    for symbol in symbols:
        f.write(symbol + "\n")
