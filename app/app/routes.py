from flask import Blueprint, jsonify, request
from app.database import execute_query, execute_on_all_nodes

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
    query = "SELECT * FROM dim_game LIMIT 10"
    results = execute_on_all_nodes(query)
    return jsonify(results)

@bp.route('/game/<int:game_id>', methods=['GET'])
def get_game(game_id):
    query = "SELECT * FROM dim_game WHERE game_id = %s"
    results = execute_on_all_nodes(query, (game_id,))
    return jsonify(results)

@bp.route('/game', methods=['POST'])
def add_game():
    data = request.json
    query = """
    INSERT INTO dim_game (game_id, name, required_age, price, metacritic_score, achievements)
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
    UPDATE dim_game
    SET price = %s
    WHERE game_id = %s
    """
    params = (data['price'], game_id)
    results = execute_on_all_nodes(query, params)
    return jsonify(results)
