from models.mba_player_model import NBAPlayer
from models.team import Team
from services.caloulter_actions import cal_atr, cal_ppg
from db import db

def get_players_from_db(position, season=None):
    """
    :param position: The position of the NBA players to be queried from the database.
    :param season: (Optional) The season of the NBA players to be queried from the database.
    :return: A list of dictionaries containing player information including player name, team, position, season, points, games, twoPercent, threePercent, ATR, and PPG Ratio.
    """
    if season:
        query = NBAPlayer.query.filter_by(position=position, season=season).all()
    else:
        query = NBAPlayer.query.filter_by(position=position).all()
    result = [{'playerName': player.playerName, 'team': player.team, 'position': player.position,
               'season': player.season, 'points': player.points, 'games': player.games,
               'twoPercent': player.twoPercent, 'threePercent': player.threePercent,
               'ATR': cal_atr(), 'PPG Ratio': cal_ppg()}
                for player in query]
    return result


def get_players_position(player_ids):
    """
    מחזיר מהדאטה בייס את כל העמדות של השחקנים לצורך בדיקה להוספת קבוצה חדשה
    בודק האם יש 5 עמדות שונות בנוסף זה יבדוק שיש את השחקנים האלו (כי אם חסר עמדה סימן שלא נמצא השחקן)
    """
    result = []
    try:
        for player_id in player_ids:
            player = NBAPlayer.query.filter_by(id=player_id).first()
            result.append(player.position)
    except Exception as e:
        print(e)

    return result

def create_new_team(team_name, players_id):
    """
    Create a new team and insert it into the database.
    :param team_name: The name of the team to be created.
    :param players_id: A list of player IDs to be added to the team.
    :return: The ID of the newly created team.
    """
    new_team = Team(
        teamName=team_name,
        player1_id=players_id[0],
        player2_id=players_id[1],
        player3_id=players_id[2],
        player4_id=players_id[3],
        player5_id=players_id[4]
    )

    db.session.add(new_team)
    db.session.commit()

    return new_team.id
