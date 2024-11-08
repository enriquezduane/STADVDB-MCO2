# app/app/database.py
import mysql.connector
from config import Config

def get_db_connection(node='central'):
    try:
        return mysql.connector.connect(**Config.DB_CONFIGS[node])
    except mysql.connector.Error as err:
        print(f"Error connecting to {node}: {err}")
        return None

def execute_query(node, query, params=None, fetch=True):
    conn = get_db_connection(node)
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid
            
        cursor.close()
        conn.close()
        return result
    except mysql.connector.Error as err:
        print(f"Query error on {node}: {err}")
        conn.close()
        return None

def execute_on_all_nodes(query, params=None):
    results = {}
    for node in Config.DB_CONFIGS.keys():
        results[node] = execute_query(node, query, params)
    return results

def get_db_connection(node='central', isolation_level='READ COMMITTED'):
    try:
        conn = mysql.connector.connect(**Config.DB_CONFIGS[node])
        conn.start_transaction(isolation_level=isolation_level)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to {node}: {err}")
        return None