from NFL_api import NFL_api
from time import sleep
import json
import os

# PURPOSE: get all data from API and save to json files 
# TODO: get and order all data
# TODO: finish downloading games 41:-1

# RUN ORDER:
# 1. download_team_stats()
# 2. download_games()
# 3. save_games_by_team() (for each team in teams)
# 4. save_game_list()
# 5. download_game_team_stats() (for each game in games) for game in list(json.load(open('../data/seasons/2022_games_list.json'))):
# 6. 

teams = json.load(open('../ids.json'))["teams"]
id_dict = dict(zip(teams.values(), teams.keys()))
list_teams = list(teams.keys())
completed_games_list = list(json.load(open('../data/seasons/2022_completed_games_list.json')))

def update_all_data(year : int):
    download_team_stats(year=year) # 32 API Calls
    download_games(year=year) # 1 API Call
    for team in list_teams:
        save_games_by_team(team, year=year) # 0 API Calls
    save_game_list() # 0 API Calls
    games_list = list(json.load(open('../data/seasons/2022_games_list.json')))
    for game in games_list:
        download_game_team_stats(game) # 272 API Calls
    with open('../data/seasons/2022_completed_games_list.json', 'w') as f:
        json.dump(completed_games_list, f)
    return

def download_team_stats(year : int = 2022, do_sleep = True):
    # TODO: test this function; has changed since last test
    for i in range(1, 33):
        print(f"Getting team {i} data")
        team_name = id_dict[i]
        api.save_to_json(api.get_team_data(i, year, format="json"), f"../data/teams/{team_name}/{year}/team_stats.json")
        if do_sleep:
            sleep(8)
    return

def download_games(year : int):
    api.save_to_json(api.get_season_games(year, format="json"), f"../data/seasons/{year}_games.json")
    return

def get_team_roster(team : str, year : int = 2022):
    assert team in list_teams, f"Team {team} not in list of teams"
    # load in team stats
    team_stats = json.load(open(f"../data/teams/{team}/{year}/team_stats.json"))["response"]
    # id : name
    players = {}
    for player in team_stats:
        players[player["player"]["id"]] = player["player"]["name"]
    return players

def save_games_by_team(team : str, year : int = 2022):
    def get_winner(PF, PA):
        if PF is None:
            return None
        return PF > PA
    ignore_stage = ["Pre Season"]
    assert team in list_teams, f"Team {team} not in list of teams"
    # load in games
    games = json.load(open(f"../data/seasons/{year}_games.json"))["response"]
    # week : {id:int, opponent:string, home:bool, PF:int. PA:int, win:bool, time:str}
    team_games = {}
    for game in games:
        if game["game"]["stage"] in ignore_stage:
            continue
        if game["teams"]["home"]["name"] == team:
            team_games[game["game"]["week"]] = {
                "id": game["game"]["id"],
                "opponent": game["teams"]["away"]["name"],
                "home": True,
                "PF": game["scores"]["home"]["total"],
                "PA": game["scores"]["away"]["total"],
                "win": get_winner(game["scores"]["home"]["total"], game["scores"]["away"]["total"]),
                "time": game["game"]["date"]["time"]
            }
        elif game["teams"]["away"]["name"] == team:
            team_games[game["game"]["week"]] = {
                "id": game["game"]["id"],
                "opponent": game["teams"]["home"]["name"],
                "home": False,
                "PF": game["scores"]["away"]["total"],
                "PA": game["scores"]["home"]["total"],
                "win": get_winner(game["scores"]["away"]["total"], game["scores"]["home"]["total"]),
                "time": game["game"]["date"]["time"]
            }
    api.save_to_json(team_games, f"../data/teams/{team}/{year}/games.json")
    return

def save_game_list(year: int = 2022):
    ignore_stage = ["Pre Season"]
    # Get list of all games
    games = json.load(open(f"../data/seasons/{year}_games.json"))["response"]
    games_list = []
    for game in games:
        if game["game"]["stage"] in ignore_stage:
            continue
        if game["game"]["status"]["short"] != "FT" and game["game"]["status"]["long"] != "Final/OT":
            continue
        games_list.append(game["game"]["id"]) # id of game
    api.save_to_json(games_list, f"../data/seasons/{year}_games_list.json")
    return

def download_game_team_stats(game_id : int, do_sleep : bool = True):
    if game_id in completed_games_list:
        return
    try:
        game_json = api.get_game_team_data(game_id, format="json")["response"]
    except:
        print(f"Error getting game {game_id}")
        with open('../data/completed_games_list.json', 'w') as f:
            json.dump(completed_games_list, f)
        return
    print(f"Getting game {game_id} data")

    home = game_json[0]
    home_team = home["team"]["name"]
    home_stats = home["statistics"]

    away = game_json[1]
    away_team = away["team"]["name"]
    away_stats = away["statistics"]

    games = json.load(open(f"../data/teams/{home_team}/2022/games.json"))
    for game in games.keys():
        if games[game]["id"] == game_id:
            week = game
            break

    # create Week X folder if it doesn't exist
    if not os.path.exists(f"../data/teams/{home_team}/2022/{week}"):
        os.makedirs(f"../data/teams/{home_team}/2022/{week}")
    if not os.path.exists(f"../data/teams/{away_team}/2022/{week}"):
        os.makedirs(f"../data/teams/{away_team}/2022/{week}")

    api.save_to_json(home_stats, f"../data/teams/{home_team}/2022/{week}/team_stats.json")
    api.save_to_json(away_stats, f"../data/teams/{away_team}/2022/{week}/team_stats.json")
    completed_games_list.append(game_id)
    if do_sleep:
        sleep(8)

if __name__ == "__main__":
    # NFL_api
    key = 'a3ca5a83a4mshe686c311350a29cp1709fcjsn80bbdbfce2f6'
    host = 'api-american-football.p.rapidapi.com'
    api = NFL_api(key, host)
    year = 2022

