from time import sleep
from api_writer import api_writer

if __name__ == "__main__":
    # api_writer
    key = "a3ca5a83a4mshe686c311350a29cp1709fcjsn80bbdbfce2f6"
    host = "alpha-vantage.p.rapidapi.com"
    writer = api_writer(key, host)
    
    with open("TSDA/_symbols.txt", "r") as f:
        symbols = f.read().splitlines()
    for symbol in symbols:
        print(symbol)
        writer.write(symbol, "full")
        sleep(15) # 5 requests per minute, 500 requests per day
