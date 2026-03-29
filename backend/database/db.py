import sqlite3
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = 'research.db'

def init_db():
    """
    Initialize the SQLite database with required tables.
    
    Tables:
    - research_queries: Stores user queries
    - research_results: Stores individual agent results
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create research_queries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create research_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER NOT NULL,
                agent_name TEXT NOT NULL,
                result_json TEXT NOT NULL,
                FOREIGN KEY (query_id) REFERENCES research_queries(id)
            )
        ''')
        
        # Create indexes for better query performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_query_id 
            ON research_results(query_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_agent_name 
            ON research_results(agent_name)
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise

def save_research(query, agent_results):
    """
    Save research query and all agent results to database.
    
    Args:
        query (str): The research query
        agent_results (dict): Dictionary containing results from all agents
        
    Returns:
        int: The query_id of the saved research
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Insert research query
        cursor.execute(
            'INSERT INTO research_queries (query, timestamp) VALUES (?, ?)',
            (query, datetime.now())
        )
        
        query_id = cursor.lastrowid
        
        # Insert results for each agent
        agent_names = [
            'retrieval',
            'extraction',
            'comparison',
            'validation',
            'gap_analysis',
            'ideation',
            'output'
        ]
        
        for agent_name in agent_names:
            if agent_name in agent_results:
                result_json = json.dumps(agent_results[agent_name])
                
                cursor.execute(
                    'INSERT INTO research_results (query_id, agent_name, result_json) VALUES (?, ?, ?)',
                    (query_id, agent_name, result_json)
                )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Research saved successfully with query_id: {query_id}")
        return query_id
        
    except Exception as e:
        logger.error(f"Error saving research: {str(e)}")
        raise

def get_research_by_id(query_id):
    """
    Retrieve a research query and all its agent results by query_id.
    
    Args:
        query_id (int): The ID of the research query
        
    Returns:
        dict: Dictionary containing query info and all agent results
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get query info
        cursor.execute(
            'SELECT id, query, timestamp FROM research_queries WHERE id = ?',
            (query_id,)
        )
        
        query_row = cursor.fetchone()
        
        if not query_row:
            conn.close()
            return None
        
        # Get all agent results
        cursor.execute(
            'SELECT agent_name, result_json FROM research_results WHERE query_id = ?',
            (query_id,)
        )
        
        results_rows = cursor.fetchall()
        
        conn.close()
        
        # Build response
        agent_results = {}
        for agent_name, result_json in results_rows:
            agent_results[agent_name] = json.loads(result_json)
        
        return {
            'id': query_row[0],
            'query': query_row[1],
            'timestamp': query_row[2],
            'agent_results': agent_results
        }
        
    except Exception as e:
        logger.error(f"Error retrieving research: {str(e)}")
        raise

def get_all_queries(limit=50):
    """
    Retrieve all research queries (without full results).
    
    Args:
        limit (int): Maximum number of queries to return
        
    Returns:
        list: List of query dictionaries
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT id, query, timestamp FROM research_queries ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        queries = []
        for row in rows:
            queries.append({
                'id': row[0],
                'query': row[1],
                'timestamp': row[2]
            })
        
        return queries
        
    except Exception as e:
        logger.error(f"Error retrieving queries: {str(e)}")
        raise

def get_agent_results(query_id, agent_name):
    """
    Retrieve results for a specific agent and query.
    
    Args:
        query_id (int): The ID of the research query
        agent_name (str): Name of the agent
        
    Returns:
        dict: Agent result data or None if not found
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT result_json FROM research_results WHERE query_id = ? AND agent_name = ?',
            (query_id, agent_name)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        
        return None
        
    except Exception as e:
        logger.error(f"Error retrieving agent results: {str(e)}")
        raise

def delete_research(query_id):
    """
    Delete a research query and all its associated results.
    
    Args:
        query_id (int): The ID of the research query to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Delete agent results first (foreign key constraint)
        cursor.execute(
            'DELETE FROM research_results WHERE query_id = ?',
            (query_id,)
        )
        
        # Delete query
        cursor.execute(
            'DELETE FROM research_queries WHERE id = ?',
            (query_id,)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Research with query_id {query_id} deleted successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error deleting research: {str(e)}")
        return False

def get_database_stats():
    """
    Get statistics about the database.
    
    Returns:
        dict: Database statistics
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Count total queries
        cursor.execute('SELECT COUNT(*) FROM research_queries')
        total_queries = cursor.fetchone()[0]
        
        # Count total results
        cursor.execute('SELECT COUNT(*) FROM research_results')
        total_results = cursor.fetchone()[0]
        
        # Get most recent query
        cursor.execute('SELECT query, timestamp FROM research_queries ORDER BY timestamp DESC LIMIT 1')
        recent = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_queries': total_queries,
            'total_results': total_results,
            'most_recent_query': recent[0] if recent else None,
            'most_recent_timestamp': recent[1] if recent else None
        }
        
    except Exception as e:
        logger.error(f"Error getting database stats: {str(e)}")
        raise
