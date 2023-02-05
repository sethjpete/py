import json
import os

teams = json.load(open('../ids.json'))
list_teams = list(teams['teams'].keys())
#
#
# USE TO SETUP FOLDERS FOR MODEL
#
#
# Generate folders for each team in ../data/teams
# If folder already exists, skip
def gen_team_folders():
    for team in list_teams:
        if not os.path.exists('../data/teams/' + team):
            os.mkdir('../data/teams/' + team)

def gen_year_folders():
    for team in list_teams:
        for year in range(2015, 2023):
            if not os.path.exists('../data/teams/' + team + '/' + str(year)):
                os.mkdir('../data/teams/' + team + '/' + str(year))

# DEPRECATED
@staticmethod
def move_and_gen():
    for team in list_teams:
        id = teams['teams'][team]
        print(team, id)
        # Move the file "team_id" to the folder "team_name"
        os.rename('../data/teams/team_' + str(id) + '.json', '../data/teams/' + team + '/team_stats.json')
        # Create a file "_info.json" in the folder "team_name"
        if not os.path.exists('../data/teams/' + team + '/_info.json'):
            with open('../data/teams/' + team + '/_info.json', 'w') as f:
                f.write('{"id": "' + str(id) + '"}')

gen_year_folders()