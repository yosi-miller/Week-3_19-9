from flask import Blueprint, request, jsonify
from db import db
from services.players_service import get_players_from_db

players_bp = Blueprint('players', __name__, url_prefix='/api')

@players_bp.route('/players', methods=['GET'])
def get_players_by_position():
    position = request.args.get('position')
    season = request.args.get('season')

    if not position or position not in ['PG', 'SG', 'SF', 'PF', 'C']:
        return jsonify({"error": "Position is required and must be one of PG, SG, SF, PF, C"}), 400

    all_players = get_players_from_db()

    # query = db.session.query(
    #     Player.playerName,
    #     Player.team,
    #     Player.position,
    #     db.func.array_agg(PlayerSeason.season).label('seasons'),
    #     db.func.sum(PlayerSeason.points).label('points'),
    #     db.func.sum(PlayerSeason.games).label('games'),
    #     db.func.avg(PlayerSeason.twoPercent).label('twoPercent'),
    #     db.func.avg(PlayerSeason.threePercent).label('threePercent'),
    #     (db.func.avg(PlayerSeason.assists) / db.func.nullif(db.func.avg(PlayerSeason.turnovers), 0)).label('ATR'),
    #     (db.func.avg(PlayerSeason.points) / db.func.nullif(db.func.avg(PlayerSeason.position_average_points), 0)).label(
    #         'PPG_Ratio')
    # ).join(PlayerSeason).filter(Player.position == position)
    #
    # if season:
    #     query = query.filter(PlayerSeason.season == season)
    #
    # query = query.group_by(Player.playerName, Player.team, Player.position)
    #
    # results = query.all()
    #
    # players = []
    # for row in results:
    #     players.append({
    #         "playerName": row.playerName,
    #         "team": row.team,
    #         "position": row.position,
    #         "seasons": row.seasons,
    #         "points": row.points,
    #         "games": row.games,
    #         "twoPercent": row.twoPercent,
    #         "threePercent": row.threePercent,
    #         "ATR": row.atr,
    #         "PPG_Ratio": row.ppg_ratio
    #     })
    if not all_players:
        return jsonify({"error": "No players found"}), 404

    return jsonify({'all_players' : 'ok'}), 200
