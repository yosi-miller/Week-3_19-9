from flask import Blueprint, request, jsonify
from db import db
from services.players_service import (
    get_players_from_db,
    get_players_position,
    create_new_team,
    update_team_in_db,
    delete_team_from_db,
    get_team_from_db,
    checks_teams_exists,
    compare_teams_by_ppg)

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

    # Checks whether there are 5 different positions.
    # In addition, it will check that these players are present
    # (because if a position is missing, it means that the player is not found)    players_position = get_players_position(player_ids)
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

    # check if have id team and 3 player
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


@players_bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team_details(team_id):
    team = get_team_from_db(team_id)

    if not team:
        return jsonify({"error": "Team not found"}), 404

    return jsonify(team), 200


@players_bp.route('/teams/compare', methods=['GET'])
def compare_teams():
    team_ids = request.args.getlist('team_id')
    print(team_ids)

    # Validate that at least 2 team IDs are provided
    if len(team_ids) < 2:
        return jsonify({"error": "At least 2 team IDs are required for comparison"}), 400

    # check if all team are exist
    teams_exists = checks_teams_exists(team_ids)
    if not teams_exists:
        return jsonify({'error': 'One or more team not exist'}), 404

    comparison_results = compare_teams_by_ppg(team_ids)

    return jsonify({"comparison": comparison_results}), 200
