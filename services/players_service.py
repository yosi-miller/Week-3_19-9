from models.mba_player_model import NBAPlayer
from models.team import Team
from services.caloulter_actions import calculator_atr, calculator_ppg
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

    result: list[dict] = [{'playerName': player.playerName,
               'team': player.team,
               'position': player.position,
               'season': player.season,
               'points': player.points,
               'games': player.games,
               'twoPercent': player.twoPercent,
               'threePercent': player.threePercent,
               'ATR': calculator_atr(player.assists, player.turnovers),
               'PPG Ratio': calculator_ppg()}

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


def update_team_in_db(team_id, player_ids):
    """
    Update the team in the database with new players.
    :param team_id: The ID of the team to be updated.
    :param player_ids: A list of new player IDs to be added to the team.
    :return: A boolean indicating whether the update was successful.
    """
    try:
        team = Team.query.filter_by(id=team_id).first()
        if not team:
            return False
    except Exception as e:
        db.session.rollback()
        return False
    else:
        team.player1_id = player_ids[0]
        team.player2_id = player_ids[1]
        team.player3_id = player_ids[2]
        team.player4_id = player_ids[3]
        team.player5_id = player_ids[4]

        db.session.commit()
        return True

def delete_team_from_db(team_id):
    try:
        team_delete = Team.query.filter_by(id=team_id).first()
        db.session.delete(team_delete)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def generate_player(player_id):
    player = NBAPlayer.query.filter_by(id=player_id).first()
    if not player:
        return {}

    result = {'playerName': player.playerName,
              'team': player.team,
              'position': player.position,
              'season': player.season,
              'points': player.points,
              'games': player.games,
              'twoPercent': player.twoPercent,
              'threePercent': player.threePercent,
              'ATR': calculator_atr(player.assists, player.turnovers),
              'PPG Ratio': calculator_ppg()}
    return result

def get_team_from_db(team_id):
    team = Team.query.filter_by(id=team_id).first()

    if not team:
        return False

    result = {'teamName': team.teamName,
              'player1_id': generate_player(team.player1_id),
              'player2_id': generate_player(team.player2_id),
              'player3_id': generate_player(team.player3_id),
              'player4_id': generate_player(team.player4_id),
              'player5_id': generate_player(team.player5_id)
              }
    return result


def checks_teams_exists(team_ids):
    """
    checks_teams_exists
    :param team_ids: list of team id
    :return: boolean
    """
    for team_id in team_ids:
        if not Team.query.filter_by(id=team_id).first():
            return False
    return True

def compare_teams_by_ppg(team_1):
    """
    compare_teams_by_ppg
    :param team_1: list of player id
    :return: dict of compare teams
    """
    pass