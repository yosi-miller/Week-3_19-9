from flask import Blueprint, request, jsonify
from db import db
from services.players_service import (
    get_players_from_db,
    get_players_position,
    create_new_team,
    update_team_in_db,
    delete_team_from_db)

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

    if not team_name or not player_ids or len(player_ids) != 5:
        return jsonify({"error": "Team name and exactly 5 player IDs are required"}), 400

    # בודק האם יש 5 עמדות שונות בנוסף זה יבדוק שיש את השחקנים האלו (כי אם חסר עמדה סימן שלא נמצא השחקן)
    players_position = get_players_position(player_ids)

    if len(set(players_position)) != 5:
        return jsonify({"error": "Each position (PG, SG, SF, PF, C) must be represented by one player"}), 400

    new_team = create_new_team(team_name, player_ids)

    if not new_team:
        return jsonify({"error": "Team could not be created"}), 400
    return jsonify(new_team), 201


@players_bp.route('/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    player_ids  = request.get_json().get('player_ids')

    if not player_ids or len(player_ids) != 5:
        return jsonify({"error": "Exactly 5 player IDs are required"}), 400

    players_position = get_players_position(player_ids)

    if len(set(players_position)) != 5:
        return jsonify({"error": "Each position (PG, SG, SF, PF, C) must be represented by one player"}), 400

    # בדיקת כפל שחקנים בקבוצות אחרות
    # if not validate_unique_players(team_id, player_ids):
    #     return jsonify({"error": "A player cannot be in more than one team"}), 400

    updated_team = update_team_in_db(team_id, player_ids)

    if not updated_team:
        return jsonify({"error": "Team could not be updated"}), 400

    return jsonify(updated_team), 200


@players_bp.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    result = delete_team_from_db(team_id)

    if result:
        return jsonify({"message": "Team deleted successfully"}), 200
    else:
        return jsonify({"error": "Team not found"}), 404