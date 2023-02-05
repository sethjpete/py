import requests

class api_writer:

    def __init__(self, key, host):
        self.key = key
        self.host = host
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.host
        }

    def write_daily_adjusted(self, symbol, outputsize):
        querystring = {"function":"TIME_SERIES_DAILY_ADJUSTED","symbol":symbol,"outputsize":"full","datatype":"csv"}
        response = requests.request("GET", self.url, headers=self.headers, params=querystring)
        
        with open("TSDA/" + symbol + ".csv", "w") as f:
            f.write(response.text)
        print(response.text[:200])