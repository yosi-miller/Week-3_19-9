from flask import Blueprint, request, jsonify
from db import db
from services.players_service import get_players_from_db, get_players_position, create_new_team

players_bp = Blueprint('players', __name__, url_prefix='/api')

@players_bp.route('/players', methods=['GET'])
def get_players_by_position():
    position = request.args.get('position')
    season = request.args.get('season')

    if not position or position not in ['PG', 'SG', 'SF', 'PF', 'C']:
        return jsonify({"error": "Position is required and must be one of PG, SG, SF, PF, C"}), 400

    all_players = get_players_from_db(position, season)

    if not all_players:
        return jsonify({"error": "No players found"}), 404

    return jsonify(all_players), 200


@players_bp.route('/teams', methods=['POST'])
def create_team():
    data = request.get_json()
    team_name = data.get('team_name')
    player_ids = data.get('player_ids')
    print(data)
    if not team_name or not player_ids or len(player_ids) != 5:
        return jsonify({"error": "Team name and exactly 5 player IDs are required"}), 400

    # בודק האם יש 5 עמדות שונות בנוסף זה יבדוק שיש את השחקנים האלו (כי אם חסר עמדה סימן שלא נמצא השחקן)
    players_position = get_players_position(player_ids)
    print(players_position)
    if len(set(players_position)) != 5:
        return jsonify({"error": "Each position (PG, SG, SF, PF, C) must be represented by one player"}), 400

    new_team = create_new_team(team_name, player_ids)

    if not new_team:
        return jsonify({"error": "Team could not be created"}), 400
    return jsonify(new_team), 201
