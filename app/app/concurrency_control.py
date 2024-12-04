from threading import Thread
from app.database import get_db_connection

def simulate_case_1():
    logs = []

    def transaction_1():
        logs.append("Transaction 1 started on node2")
        conn = get_db_connection('node2', 'READ COMMITTED')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM games_for_everyone WHERE game_id = 1")
        result = cursor.fetchone()
        logs.append(f"Transaction 1 result on node2: {result}")
        cursor.close()
        conn.close()
        logs.append("Transaction 1 completed on node2")

    def transaction_2():
        logs.append("Transaction 2 started on node3")
        conn = get_db_connection('node3', 'READ COMMITTED')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM games_for_adults WHERE game_id = 1")
        result = cursor.fetchone()
        logs.append(f"Transaction 2 result on node3: {result}")
        cursor.close()
        conn.close()
        logs.append("Transaction 2 completed on node3")

    t1 = Thread(target=transaction_1)
    t2 = Thread(target=transaction_2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    return logs

def simulate_case_2():
    logs = []

    def transaction_1():
        logs.append("Transaction 1 started on node2")
        conn = get_db_connection('node2', 'READ COMMITTED')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM games WHERE game_id = 1")
        result = cursor.fetchone()
        logs.append(f"Transaction 1 result on node2: {result}")
        cursor.close()
        conn.close()
        logs.append("Transaction 1 completed on node2")

    def transaction_2():
        logs.append("Transaction 2 started on node3")
        conn = get_db_connection('node3', 'READ COMMITTED')
        cursor = conn.cursor()
        cursor.execute("UPDATE games SET price = price + 1 WHERE game_id = 1")
        conn.commit()
        logs.append("Transaction 2 updated price on node3")
        cursor.close()
        conn.close()
        logs.append("Transaction 2 completed on node3")

    t1 = Thread(target=transaction_1)
    t2 = Thread(target=transaction_2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    return logs

def simulate_case_3():
    logs = []

    def transaction_1():
        logs.append("Transaction 1 started on node2")
        conn = get_db_connection('node2', 'SERIALIZABLE')
        cursor = conn.cursor()
        cursor.execute("UPDATE games SET price = price + 1 WHERE game_id = 1")
        conn.commit()
        logs.append("Transaction 1 updated price on node2")
        cursor.close()
        conn.close()
        logs.append("Transaction 1 completed on node2")

    def transaction_2():
        logs.append("Transaction 2 started on node3")
        conn = get_db_connection('node3', 'SERIALIZABLE')
        cursor = conn.cursor()
        cursor.execute("UPDATE games SET price = price + 1 WHERE game_id = 1")
        conn.commit()
        logs.append("Transaction 2 updated price on node3")
        cursor.close()
        conn.close()
        logs.append("Transaction 2 completed on node3")

    t1 = Thread(target=transaction_1)
    t2 = Thread(target=transaction_2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Check final state of the database
    final_state_logs = []
    for node in ['central', 'node2', 'node3']:
        conn = get_db_connection(node, 'READ COMMITTED')
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM games WHERE game_id = 1")
        result = cursor.fetchone()
        final_state_logs.append(f"Final price on {node}: {result[0]}")
        cursor.close()
        conn.close()

    logs.extend(final_state_logs)
    return logs