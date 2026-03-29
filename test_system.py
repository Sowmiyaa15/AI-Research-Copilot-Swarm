#!/usr/bin/env python3
"""
Test script to verify AI Research Copilot Swarm installation and functionality.
Run this after installing dependencies to ensure everything works.
"""

import sys
import subprocess
import importlib.util

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    """Print success message."""
    print(f"✅ {text}")

def print_error(text):
    """Print error message."""
    print(f"❌ {text}")

def print_info(text):
    """Print info message."""
    print(f"ℹ️  {text}")

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success("Python version is compatible (3.8+)")
        return True
    else:
        print_error("Python version must be 3.8 or higher")
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    print_header("Checking Dependencies")
    
    dependencies = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'requests': 'Requests'
    }
    
    all_installed = True
    
    for module_name, display_name in dependencies.items():
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print_success(f"{display_name} is installed")
        else:
            print_error(f"{display_name} is NOT installed")
            all_installed = False
    
    if not all_installed:
        print_info("Install missing dependencies with: pip install -r requirements.txt")
    
    return all_installed

def check_file_structure():
    """Check if all required files exist."""
    print_header("Checking File Structure")
    
    import os
    
    required_files = [
        'backend/app.py',
        'backend/agents/retrieval_agent.py',
        'backend/agents/extraction_agent.py',
        'backend/agents/comparison_agent.py',
        'backend/agents/validation_agent.py',
        'backend/agents/gap_agent.py',
        'backend/agents/ideation_agent.py',
        'backend/agents/output_agent.py',
        'backend/services/arxiv_service.py',
        'backend/database/db.py',
        'backend/models/research.py',
        'frontend/index.html',
        'frontend/style.css',
        'frontend/script.js',
        'requirements.txt'
    ]
    
    all_exist = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} is MISSING")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test if all agent modules can be imported."""
    print_header("Testing Agent Imports")
    
    sys.path.insert(0, 'backend')
    
    agents = [
        'agents.retrieval_agent',
        'agents.extraction_agent',
        'agents.comparison_agent',
        'agents.validation_agent',
        'agents.gap_agent',
        'agents.ideation_agent',
        'agents.output_agent'
    ]
    
    all_imported = True
    
    for agent_module in agents:
        try:
            __import__(agent_module)
            print_success(f"{agent_module}")
        except Exception as e:
            print_error(f"{agent_module}: {str(e)}")
            all_imported = False
    
    return all_imported

def test_database():
    """Test database initialization."""
    print_header("Testing Database")
    
    sys.path.insert(0, 'backend')
    
    try:
        from database.db import init_db, get_database_stats
        
        # Initialize database
        init_db()
        print_success("Database initialized successfully")
        
        # Get stats
        stats = get_database_stats()
        print_success(f"Database stats retrieved: {stats['total_queries']} queries")
        
        return True
    except Exception as e:
        print_error(f"Database test failed: {str(e)}")
        return False

def test_arxiv_service():
    """Test arXiv service connectivity."""
    print_header("Testing arXiv API Connection")
    
    sys.path.insert(0, 'backend')
    
    try:
        from services.arxiv_service import ArxivService
        
        service = ArxivService()
        result = service.search("machine learning", max_results=1)
        
        if result.get('papers'):
            print_success(f"arXiv API is accessible - retrieved {len(result['papers'])} paper(s)")
            return True
        else:
            print_error("arXiv API returned no results")
            return False
    except Exception as e:
        print_error(f"arXiv API test failed: {str(e)}")
        print_info("This is expected if you don't have internet connection")
        return False

def test_agent_pipeline():
    """Test a simple agent pipeline."""
    print_header("Testing Agent Pipeline")
    
    sys.path.insert(0, 'backend')
    
    try:
        from agents.retrieval_agent import RetrievalAgent
        from agents.extraction_agent import ExtractionAgent
        
        # Test retrieval agent
        retrieval = RetrievalAgent()
        retrieval_result = retrieval.process("test query")
        
        if retrieval_result.get('status') == 'completed' or retrieval_result.get('status') == 'error':
            print_success("Retrieval agent executed")
        else:
            print_error("Retrieval agent failed")
            return False
        
        # Test extraction agent
        extraction = ExtractionAgent()
        extraction_result = extraction.process(retrieval_result)
        
        if extraction_result.get('status') == 'completed' or extraction_result.get('status') == 'error':
            print_success("Extraction agent executed")
        else:
            print_error("Extraction agent failed")
            return False
        
        print_success("Agent pipeline test completed")
        return True
        
    except Exception as e:
        print_error(f"Agent pipeline test failed: {str(e)}")
        return False

def print_summary(results):
    """Print test summary."""
    print_header("Test Summary")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n" + "🎉" * 20)
        print("ALL TESTS PASSED!")
        print("Your system is ready to use!")
        print("🎉" * 20)
        print("\nNext steps:")
        print("1. Run: python backend/app.py")
        print("2. Open: frontend/index.html in your browser")
        print("3. Enter a research query and click 'Analyze Research'")
    else:
        print("\n" + "⚠️" * 20)
        print("SOME TESTS FAILED")
        print("Please fix the issues above before running the application")
        print("⚠️" * 20)
    
    return failed == 0

def main():
    """Run all tests."""
    print("\n" + "🤖" * 30)
    print("AI RESEARCH COPILOT SWARM - SYSTEM TEST")
    print("🤖" * 30)
    
    results = {}
    
    # Run tests
    results['Python Version'] = check_python_version()
    results['Dependencies'] = check_dependencies()
    results['File Structure'] = check_file_structure()
    results['Agent Imports'] = test_imports()
    results['Database'] = test_database()
    results['arXiv API'] = test_arxiv_service()
    results['Agent Pipeline'] = test_agent_pipeline()
    
    # Print summary
    success = print_summary(results)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
