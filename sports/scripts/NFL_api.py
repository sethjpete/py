import requests
import json

# TODO: Reset calls every day

class NFL_api:
    max_calls = 100
    permit_overage = True
    max_overage = 350

    def __init__(self, key, host):
        self.key = key
        self.host = host
        self.calls = self.__update_calls()
    
    def __update_calls(self) -> int:
        with open('../data/_calls.txt', 'r') as f:
            calls = int(f.read())
            print(f'Calls: {calls}')
        return calls

    def __request(self, type :str, url : str, headers : dict, params : str) -> requests.models.Response:
        print(f"Calls: {self.calls}")

        if self.calls >= self.max_calls and not self.permit_overage:
            print('Max calls reached')
            return None
        elif self.calls >= self.max_calls and self.permit_overage:
            print('Max calls reached, but overage is permitted')
            self.permit_overage = False
            self.max_calls += self.max_overage

        response = requests.request(type, url, headers=headers, params=params)
        self.calls += 1
        with open('../data/_calls.txt', 'w') as f:
            f.write(str(self.calls))

        return response

    # Unnecessary due to get_team_data
    def get_player_data(self, player_id :int, season : int, format : str = 'text'):
        url = "https://api-american-football.p.rapidapi.com/players/statistics"
        
        querystring = {"season": season,"id":player_id}
        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.host
        }
        
        response = self.__request("GET", url, headers=headers, params=querystring)
        if format == 'json':
            return response.json()
        return response.text

    # Generally useless API call
    def get_team_data(self, team_id :int, format : str = 'text'):
        url = "https://api-american-football.p.rapidapi.com/teams"

        querystring = {"id":team_id}
        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.host
        }
        
        response = self.__request("GET", url, headers=headers, params=querystring)
        if format == 'json':
            return response.json()
        return response.text
    
    def get_team_player_data(self, team_id :int, season : int, format : str = 'text'):
        url = "https://api-american-football.p.rapidapi.com/players/statistics"

        querystring = {"season": season,"team":team_id}
        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.host
        }
        
        response = self.__request("GET", url, headers=headers, params=querystring)
        if format == 'json':
            return response.json()
        return response.text
    
    def get_season_games(self, season : int, format : str = 'text'):
        url = "https://api-american-football.p.rapidapi.com/games"

        querystring = {"season":season, "league":1}
        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.host
        }
        
        response = self.__request("GET", url, headers=headers, params=querystring)
        if format == 'json':
            return response.json()
        return response.text

    def get_game_team_data(self, game_id : int, format : str = 'text'):
        url = "https://api-american-football.p.rapidapi.com/games/statistics/teams"

        querystring = {"id":game_id}
        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.host
        }

        response = self.__request("GET", url, headers=headers, params=querystring)
        if format == 'json':
            return response.json()
        return response.text

    def save_to_json(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)