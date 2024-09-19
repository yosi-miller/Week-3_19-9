# make get request to NMA players
from requests import get
from db import db
from models.mba_player_model import NBAPlayer


def get_players(year):
    """
    get players from NBA to 3 season
    :return:
    """
    URL = f'http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?season={year}&&pageSize=1000'
    try:
        response = get(URL)
    except Exception as e:
        print(e)
    else:
        return response.json()

def save_players(players):
    for player in players:
        # new_player = NBAPlayer(**player)
        new_player = NBAPlayer(
            playerName=player["playerName"],
            position=player["position"],
            games=player["games"],
            gamesStarted=player["gamesStarted"],
            minutesPg=player["minutesPg"],
            fieldGoals=player["fieldGoals"],
            fieldAttempts=player["fieldAttempts"],
            fieldPercent=player["fieldPercent"],
            threeFg=player["threeFg"],
            threeAttempts=player["threeAttempts"],
            threePercent=player["threePercent"],
            twoFg=player["twoFg"],
            twoAttempts=player["twoAttempts"],
            twoPercent=player["twoPercent"],
            effectFgPercent=player["effectFgPercent"],
            ft=player["ft"],
            ftAttempts=player["ftAttempts"],
            # ftPercent=player.get("ftPercent", 0.0),
            offensiveRb=player["offensiveRb"],
            defensiveRb=player["defensiveRb"],
            totalRb=player["totalRb"],
            assists=player["assists"],
            steals=player["steals"],
            blocks=player["blocks"],
            turnovers=player["turnovers"],
            personalFouls=player["personalFouls"],
            points=player["points"],
            team=player["team"],
            season=player["season"],
            playerId=player["playerId"]
        )
        db.session.add(new_player)
        print(f'player: {new_player.playerName} added!')
    db.session.commit()

def fetch_players():
    """
    Fetches player data for the specified years.

    The function iterates over the years 2019, 2020, and 2021,
    retrieves the player data for each year by calling `get_players`
    and then saves the retrieved data using `save_players`.

    :return: None
    """

    players_count = NBAPlayer.query.count()

    if players_count == 0:
        for year in [2022, 2023, 2024]:
            get_year_players = get_players(year)
            if get_year_players:
                save_players(get_year_players)
    else:
        print("Database already has players data.")


if __name__ == '__main__':
    # player_24 = get_players(2024)
    # print(player_24)
    fetch_players()