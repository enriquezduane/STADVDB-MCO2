from flask import Blueprint, jsonify, request
from app.database import execute_query, execute_on_all_nodes
from app.concurrency_control import simulate_case_1, simulate_case_2, simulate_case_3
from app.failure_recovery import fail_recover_1, fail_recover_2, fail_recover_3, fail_recover_4

bp = Blueprint('main', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    results = {}
    for node in ['central', 'node2', 'node3']:
        query = "SELECT 1"
        result = execute_query(node, query)
        results[node] = "healthy" if result else "unhealthy"
    return jsonify(results)

@bp.route('/games', methods=['GET'])
def get_games():
    query = "SELECT * FROM games"
    results = execute_on_all_nodes(query)
    return jsonify(results)

@bp.route('/games/adult', methods=['GET'])
def get_adult_games():
    query = "SELECT * FROM games_for_adults"
    results = execute_on_all_nodes(query)
    return jsonify(results)

@bp.route('/games/everyone', methods=['GET'])
def get_everyone_games():
    query = "SELECT * FROM games_for_everyone"
    results = execute_on_all_nodes(query)
    return jsonify(results)

@bp.route('/game/<int:game_id>', methods=['GET'])
def get_game(game_id):
    query = "SELECT * FROM games WHERE game_id = %s"
    results = execute_on_all_nodes(query, (game_id,))
    return jsonify(results)

@bp.route('/game/adult/<int:game_id>', methods=['GET'])
def get_adult_game(game_id):
    query = "SELECT * FROM games_for_adults WHERE game_id = %s"
    results = execute_on_all_nodes(query, (game_id,))
    return jsonify(results)

@bp.route('/game/everyone/<int:game_id>', methods=['GET'])
def get_everyone_game(game_id):
    query = "SELECT * FROM games_for_everyone WHERE game_id = %s"
    results = execute_on_all_nodes(query, (game_id,))
    return jsonify(results)

@bp.route('/game', methods=['POST'])
def add_game():
    data = request.json
    query = """
    INSERT INTO games (game_id, name, required_age, price, metacritic_score, achievements)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        data['game_id'],
        data['name'],
        data['required_age'],
        data['price'],
        data['metacritic_score'],
        data['achievements']
    )
    results = execute_on_all_nodes(query, params)
    return jsonify(results)

@bp.route('/game/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    data = request.json
    query = """
    UPDATE games
    SET price = %s
    WHERE game_id = %s
    """
    params = (data['price'], game_id)
    results = execute_on_all_nodes(query, params)
    return jsonify(results)

@bp.route('/simulate_case_1', methods=['GET'])
def simulate_case_1_route():
    logs = simulate_case_1()
    return jsonify({"status": "Case 1 simulation complete", "logs": logs})

@bp.route('/simulate_case_2', methods=['GET'])
def simulate_case_2_route():
    logs = simulate_case_2()
    return jsonify({"status": "Case 2 simulation complete", "logs": logs})

@bp.route('/simulate_case_3', methods=['GET'])
def simulate_case_3_route():
    logs = simulate_case_3()
    return jsonify({"status": "Case 3 simulation complete", "logs": logs})

@bp.route('/fail_recover_1', methods=['GET'])
def fail_recover_1_route():
    logs = fail_recover_1()
    return jsonify({"status": "Case 1 fail recover simulation complete", "logs": logs})

@bp.route('/fail_recover_2', methods=['GET'])
def fail_recover_2_route():
    logs = fail_recover_2()
    return jsonify({"status": "Case 2 fail recover simulation complete", "logs": logs})

@bp.route('/fail_recover_3', methods=['GET'])
def fail_recover_3_route():
    logs = fail_recover_3()
    return jsonify({"status": "Case 3 fail recover simulation complete", "logs": logs})

@bp.route('/fail_recover_4', methods=['GET'])
def fail_recover_4_route():
    logs = fail_recover_4()
    return jsonify({"status": "Case 4 fail recover simulation complete", "logs": logs})
