from .helpers import TeamGenerator

# create 10 teams with 10 players each

teams = TeamGenerator("PRT", num_teams=10).generate()

for team in teams:
    print(team)
    for player in team.players:
        print(player)
