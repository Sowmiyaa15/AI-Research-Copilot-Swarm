from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback

from agents.retrieval_agent import RetrievalAgent
from agents.extraction_agent import ExtractionAgent
from agents.comparison_agent import ComparisonAgent
from agents.validation_agent import ValidationAgent
from agents.gap_agent import GapAgent
from agents.ideation_agent import IdeationAgent
from agents.output_agent import OutputAgent
from database.db import (
    init_db, save_research, get_research_by_id, 
    get_all_queries, get_agent_results, delete_research,
    get_database_stats
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend communication
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Database initialization failed: {str(e)}")


@app.route('/api/research', methods=['POST', 'OPTIONS'])
def process_research():
    """
    Main endpoint for research analysis.
    
    Input: {"query": "AI in healthcare"}
    Output: Structured JSON with all agent results
    """
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Parse request
        data = request.json
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must be JSON'
            }), 400
        
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'error': 'Query is required',
                'message': 'Please provide a research query'
            }), 400
        
        logger.info(f"Processing research query: {query}")
        
        # Initialize results dictionary
        agent_results = {}
        
        # Agent 1: Retrieval Agent
        logger.info("Step 1/7: Running Retrieval Agent")
        retrieval_agent = RetrievalAgent()
        agent_results['retrieval'] = retrieval_agent.process(query)
        
        if agent_results['retrieval'].get('status') == 'error':
            logger.warning("Retrieval agent encountered an error")
        
        # Agent 2: Extraction Agent
        logger.info("Step 2/7: Running Extraction Agent")
        extraction_agent = ExtractionAgent()
        agent_results['extraction'] = extraction_agent.process(agent_results['retrieval'])
        
        # Agent 3: Comparison Agent
        logger.info("Step 3/7: Running Comparison Agent")
        comparison_agent = ComparisonAgent()
        agent_results['comparison'] = comparison_agent.process(agent_results['extraction'])
        
        # Agent 4: Validation Agent
        logger.info("Step 4/7: Running Validation Agent")
        validation_agent = ValidationAgent()
        agent_results['validation'] = validation_agent.process(agent_results['comparison'])
        
        # Agent 5: Gap Analysis Agent
        logger.info("Step 5/7: Running Gap Analysis Agent")
        gap_agent = GapAgent()
        agent_results['gap_analysis'] = gap_agent.process(agent_results['validation'])
        
        # Agent 6: Ideation Agent
        logger.info("Step 6/7: Running Ideation Agent")
        ideation_agent = IdeationAgent()
        agent_results['ideation'] = ideation_agent.process(agent_results['gap_analysis'])
        
        # Agent 7: Output Agent
        logger.info("Step 7/7: Running Output Agent")
        output_agent = OutputAgent()
        final_output = output_agent.process(agent_results)
        
        # Save to database
        try:
            query_id = save_research(query, agent_results)
            logger.info(f"Research results saved to database with ID: {query_id}")
        except Exception as e:
            logger.error(f"Failed to save to database: {str(e)}")
            query_id = None
        
        # Return final structured output
        logger.info("Research analysis completed successfully")
        
        return jsonify({
            'success': True,
            'query_id': query_id,
            'query': query,
            'results': final_output.get('output', {}),
            'agent_details': agent_results,
            'message': 'Research analysis completed successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing research query: {str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e),
            'details': 'An error occurred while processing your request'
        }), 500


@app.route('/api/research/<int:query_id>', methods=['GET'])
def get_research(query_id):
    """
    Retrieve a specific research query and its results by ID.
    """
    try:
        research = get_research_by_id(query_id)
        
        if not research:
            return jsonify({
                'error': 'Not found',
                'message': f'Research with ID {query_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'research': research
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving research: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/research/<int:query_id>', methods=['DELETE'])
def delete_research_endpoint(query_id):
    """
    Delete a specific research query and its results.
    """
    try:
        success = delete_research(query_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Research with ID {query_id} deleted successfully'
            }), 200
        else:
            return jsonify({
                'error': 'Delete failed',
                'message': 'Could not delete research'
            }), 500
        
    except Exception as e:
        logger.error(f"Error deleting research: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/queries', methods=['GET'])
def list_queries():
    """
    List all research queries (without full results).
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        queries = get_all_queries(limit)
        
        return jsonify({
            'success': True,
            'count': len(queries),
            'queries': queries
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing queries: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/research/<int:query_id>/agent/<agent_name>', methods=['GET'])
def get_agent_result(query_id, agent_name):
    """
    Retrieve results for a specific agent and query.
    """
    try:
        result = get_agent_results(query_id, agent_name)
        
        if not result:
            return jsonify({
                'error': 'Not found',
                'message': f'Results for agent {agent_name} in query {query_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'agent_name': agent_name,
            'query_id': query_id,
            'result': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving agent results: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def database_stats():
    """
    Get database statistics.
    """
    try:
        stats = get_database_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'AI Research Copilot Swarm',
        'version': '1.0.0',
        'agents': [
            'Retrieval Agent',
            'Extraction Agent',
            'Comparison Agent',
            'Validation Agent',
            'Gap Analysis Agent',
            'Ideation Agent',
            'Output Agent'
        ]
    }), 200


@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List all available agents and their descriptions."""
    return jsonify({
        'agents': [
            {
                'name': 'Retrieval Agent',
                'description': 'Retrieves research papers from arXiv API',
                'order': 1
            },
            {
                'name': 'Extraction Agent',
                'description': 'Extracts key findings, methods, and problem domains',
                'order': 2
            },
            {
                'name': 'Comparison Agent',
                'description': 'Compares methods and identifies strengths/weaknesses',
                'order': 3
            },
            {
                'name': 'Validation Agent',
                'description': 'Validates consistency of claims across papers',
                'order': 4
            },
            {
                'name': 'Gap Analysis Agent',
                'description': 'Identifies research gaps and opportunities',
                'order': 5
            },
            {
                'name': 'Ideation Agent',
                'description': 'Generates research ideas and solutions',
                'order': 6
            },
            {
                'name': 'Output Agent',
                'description': 'Combines and formats all results',
                'order': 7
            }
        ]
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    logger.info("Starting AI Research Copilot Swarm backend server")
    logger.info("Server running on http://localhost:5000")
    logger.info("API endpoint: POST http://localhost:5000/api/research")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
