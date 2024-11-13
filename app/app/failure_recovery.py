import time
from contextlib import contextmanager
from mysql.connector import Error
from app.database import get_db_connection, execute_query
from copy import deepcopy

class TransactionLog:
    def __init__(self):
        self.pending_transactions = {}
        self.completed_transactions = {}

    def add_pending(self, tx_id, nodes, query, params):
        self.pending_transactions[tx_id] = {
            'nodes': set(nodes),  # Use set for nodes
            'query': query,
            'params': params,
            'status': 'pending',
            'completed_nodes': set(),
            'timestamp': time.time()
        }

    def mark_completed(self, tx_id, node):
        if tx_id in self.pending_transactions:
            tx = self.pending_transactions[tx_id]
            tx['completed_nodes'].add(node)
            if tx['completed_nodes'] == tx['nodes']:
                self.completed_transactions[tx_id] = deepcopy(tx)
                del self.pending_transactions[tx_id]

    def get_pending_for_node(self, node):
        """Get all pending transactions for a specific node"""
        return {
            tx_id: tx for tx_id, tx in self.pending_transactions.items()
            if node in tx['nodes'] and node not in tx['completed_nodes']
        }

transaction_log = TransactionLog()

def recover_node(node):
    """Enhanced recovery function"""
    pending_txs = transaction_log.get_pending_for_node(node)
    results = []
    
    for tx_id, tx in pending_txs.items():
        success, _ = execute_safe_query(node, tx['query'], tx['params'])
        if success:
            transaction_log.mark_completed(tx_id, node)
            results.append(f"Recovered transaction {tx_id} on {node}")
        else:
            results.append(f"Failed to recover transaction {tx_id} on {node}")
    
    return results

def execute_safe_query(node, query, params):
    """Safely execute a query and handle errors"""
    try:
        result = execute_query(node, query, params, fetch=False)
        return True, result
    except Exception as e:
        print(f"Query execution failed on {node}: {str(e)}")
        return False, None

def simulate_node_failure(node):
    """Simulate a node failure by closing all connections"""
    try:
        conn = get_db_connection(node)
        if conn:
            conn.close()
        return f"Node {node} simulated failure"
    except Exception as e:
        return f"Error simulating failure for {node}: {str(e)}"

def simulate_node_recovery(node, tx_id=None):
    """Enhanced node recovery simulation"""
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            conn = get_db_connection(node)
            if conn:
                recovery_results = recover_node(node)
                conn.close()
                return f"Node {node} recovered successfully: {'; '.join(recovery_results)}"
        except Exception as e:
            print(f"Recovery attempt {attempt + 1} failed: {str(e)}")
        time.sleep(retry_delay)
    
    return f"Failed to recover node {node} after {max_retries} attempts"

def recover_specific_transaction(node, tx_id):
    """Recover a specific transaction for a node"""
    if tx_id in transaction_log.pending_transactions:
        tx_info = transaction_log.pending_transactions[tx_id]
        if node in tx_info['nodes'] and node not in tx_info['completed_nodes']:
            success, _ = execute_safe_query(node, tx_info['query'], tx_info['params'])
            if success:
                transaction_log.mark_completed(tx_id, node)

def recover_all_pending_transactions(node):
    """Recover all pending transactions for a node"""
    pending_tx_ids = list(transaction_log.pending_transactions.keys())
    for tx_id in pending_tx_ids:
        recover_specific_transaction(node, tx_id)

def fail_recover_1():
    """Simulate central node failure during transaction"""
    logs = []
    tx_id = str(time.time())
    
    try:
        query = "INSERT INTO games (game_id, name) VALUES (%s, %s)"
        params = (999, "Test Game")
        
        logs.append("Starting transaction across all nodes...")
        
        # Simulate central node failure
        logs.append("Simulating central node failure...")
        logs.append(simulate_node_failure('central'))
        
        # Add transaction to log
        transaction_log.add_pending(tx_id, ['central', 'node2', 'node3'], query, params)
        logs.append(f"Transaction {tx_id} added to pending log")
        
        # Execute on available nodes
        logs.append("Executing transaction on available nodes (node2, node3)...")
        for node in ['node2', 'node3']:
            success, _ = execute_safe_query(node, query, params)
            if success:
                transaction_log.mark_completed(tx_id, node)
                logs.append(f"Transaction completed successfully on {node}")
            else:
                logs.append(f"Transaction failed on {node}")
        
        # Recover central node and sync data
        logs.append("Attempting to recover central node...")
        recovery_result = simulate_node_recovery('central', tx_id)
        logs.append(recovery_result)
        
        # Explicitly sync data to central node
        if "recovered successfully" in recovery_result:
            success, _ = execute_safe_query('central', query, params)
            if success:
                logs.append("Data successfully synced to central node")
                transaction_log.mark_completed(tx_id, 'central')
        
        # Verify final state
        logs.append("Verifying final state...")
        for node in ['central', 'node2', 'node3']:
            result = execute_query(node, "SELECT * FROM games WHERE game_id = %s", (999,))
            logs.append(f"Data on {node}: {'Present' if result else 'Not present'}")
            if not result:
                # Retry sync if data is missing
                success, _ = execute_safe_query(node, query, params)
                if success:
                    logs.append(f"Data resynced to {node}")
        
    except Exception as e:
        logs.append(f"Error in case 1: {str(e)}")
    
    return logs

def fail_recover_2():
    """Simulate node2 failure during transaction"""
    logs = []
    tx_id = str(time.time())
    
    try:
        query = "INSERT INTO games (game_id, name) VALUES (%s, %s)"
        params = (998, "Test Game 2")
        
        logs.append("Starting transaction across all nodes...")
        
        # Simulate node2 failure
        logs.append("Simulating node2 failure...")
        logs.append(simulate_node_failure('node2'))
        
        transaction_log.add_pending(tx_id, ['central', 'node2', 'node3'], query, params)
        logs.append(f"Transaction {tx_id} added to pending log")
        
        # Execute on available nodes
        logs.append("Executing transaction on available nodes (central, node3)...")
        for node in ['central', 'node3']:
            success, _ = execute_safe_query(node, query, params)
            if success:
                transaction_log.mark_completed(tx_id, node)
                logs.append(f"Transaction completed successfully on {node}")
            else:
                logs.append(f"Transaction failed on {node}")
        
        # Recover node2
        logs.append("Attempting to recover node2...")
        logs.append(simulate_node_recovery('node2', tx_id))
        
        # Verify final state
        logs.append("Verifying final state...")
        for node in ['central', 'node2', 'node3']:
            result = execute_query(node, "SELECT * FROM games WHERE game_id = %s", (998,))
            logs.append(f"Data on {node}: {'Present' if result else 'Not present'}")
        
    except Exception as e:
        logs.append(f"Error in case 2: {str(e)}")
    
    return logs

def fail_recover_3():
    """Simulate failure in writing to central node during replication"""
    logs = []
    tx_id = str(time.time())
    
    try:
        query = "INSERT INTO games (game_id, name) VALUES (%s, %s)"
        params = (997, "Test Game 3")
        
        logs.append("Starting transaction on node2...")
        
        # Execute on node2 first
        success, _ = execute_safe_query('node2', query, params)
        if success:
            logs.append("Transaction completed successfully on node2")
            
            # Simulate central node failure during replication
            logs.append("Simulating central node failure during replication...")
            logs.append(simulate_node_failure('central'))
            
            transaction_log.add_pending(tx_id, ['central'], query, params)
            logs.append(f"Transaction {tx_id} added to pending log for central")
            
            # Recover central and retry replication
            logs.append("Attempting to recover central node...")
            logs.append(simulate_node_recovery('central', tx_id))
            
            # Verify final state
            logs.append("Verifying final state...")
            for node in ['central', 'node2']:
                result = execute_query(node, "SELECT * FROM games WHERE game_id = %s", (997,))
                logs.append(f"Data on {node}: {'Present' if result else 'Not present'}")
        else:
            logs.append("Initial transaction failed on node2")
            
    except Exception as e:
        logs.append(f"Error in case 3: {str(e)}")
    
    return logs

def fail_recover_4():
    """Simulate failure in writing to node2 during replication"""
    logs = []
    tx_id = str(time.time())
    
    try:
        query = "INSERT INTO games (game_id, name) VALUES (%s, %s)"
        params = (996, "Test Game 4")
        
        logs.append("Starting transaction on central node...")
        
        # Execute on central first
        success, _ = execute_safe_query('central', query, params)
        if success:
            logs.append("Transaction completed successfully on central")
            
            # Simulate node2 failure during replication
            logs.append("Simulating node2 failure during replication...")
            logs.append(simulate_node_failure('node2'))
            
            transaction_log.add_pending(tx_id, ['node2'], query, params)
            logs.append(f"Transaction {tx_id} added to pending log for node2")
            
            # Recover node2 and retry replication
            logs.append("Attempting to recover node2...")
            logs.append(simulate_node_recovery('node2', tx_id))
            
            # Verify final state
            logs.append("Verifying final state...")
            for node in ['central', 'node2']:
                result = execute_query(node, "SELECT * FROM games WHERE game_id = %s", (996,))
                logs.append(f"Data on {node}: {'Present' if result else 'Not present'}")
        else:
            logs.append("Initial transaction failed on central")
            
    except Exception as e:
        logs.append(f"Error in case 4: {str(e)}")
    
    return logs
