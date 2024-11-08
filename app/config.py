class Config:
    DB_CONFIGS = {
        'central': {
            'host': 'mysql-central',
            'port': 3306,
            'user': 'root',
            'password': 'rootpassword',
            'database': 'steam_games_data_warehouse'
        },
        'node2': {
            'host': 'mysql-node2',
            'port': 3306,
            'user': 'root',
            'password': 'rootpassword',
            'database': 'steam_games_data_warehouse'
        },
        'node3': {
            'host': 'mysql-node3',
            'port': 3306,
            'user': 'root',
            'password': 'rootpassword',
            'database': 'steam_games_data_warehouse'
        }
    }
