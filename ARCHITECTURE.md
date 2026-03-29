# AI Research Copilot Swarm - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                     (frontend/index.html)                       │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Input Query  │→ │   Submit     │→ │   Display    │        │
│  │              │  │   Button     │  │   Results    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    HTTP POST /api/research
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK BACKEND SERVER                       │
│                       (backend/app.py)                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              AGENT PROCESSING PIPELINE                   │ │
│  │                                                          │ │
│  │  1. Retrieval Agent    → Fetch papers from arXiv       │ │
│  │           ↓                                             │ │
│  │  2. Extraction Agent   → Extract methods & findings    │ │
│  │           ↓                                             │ │
│  │  3. Comparison Agent   → Compare methodologies         │ │
│  │           ↓                                             │ │
│  │  4. Validation Agent   → Validate claims               │ │
│  │           ↓                                             │ │
│  │  5. Gap Agent          → Identify research gaps        │ │
│  │           ↓                                             │ │
│  │  6. Ideation Agent     → Generate research ideas       │ │
│  │           ↓                                             │ │
│  │  7. Output Agent       → Format final results          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              ↓                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                   SQLite DATABASE                        │ │
│  │                                                          │ │
│  │  research_queries:                                       │ │
│  │    - id, query, timestamp                               │ │
│  │                                                          │ │
│  │  research_results:                                       │ │
│  │    - id, query_id, agent_name, result_json             │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    JSON Response with Results
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND DISPLAY                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 📊 Executive Summary                                     │ │
│  │ 📚 Retrieved Papers (5 cards)                           │ │
│  │ 🔬 Knowledge Extraction (per paper)                     │ │
│  │ ⚖️ Method Comparison (strengths/weaknesses)             │ │
│  │ ✅ Claim Validation (consistent/conflicting)            │ │
│  │ 🔍 Research Gaps (categorized)                          │ │
│  │ 💡 Research Ideas (with impact ratings)                 │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Input → Backend
```
User Query: "machine learning in healthcare"
    ↓
Frontend (script.js)
    ↓
fetch('http://localhost:5000/api/research', {
    method: 'POST',
    body: JSON.stringify({ query: "..." })
})
    ↓
Backend receives request
```

### 2. Agent Pipeline Processing

```
Query → Agent 1 (Retrieval)
    ↓
    Output: {papers: [...], papers_found: 5}
    ↓
Agent 2 (Extraction)
    ↓
    Output: {extracted_knowledge: [...]}
    ↓
Agent 3 (Comparison)
    ↓
    Output: {method_comparison: {...}}
    ↓
Agent 4 (Validation)
    ↓
    Output: {validation: {...}}
    ↓
Agent 5 (Gap Analysis)
    ↓
    Output: {research_gaps: [...]}
    ↓
Agent 6 (Ideation)
    ↓
    Output: {research_ideas: [...]}
    ↓
Agent 7 (Output)
    ↓
    Final Output: {
        retrieved_papers: {...},
        extracted_knowledge: {...},
        method_comparison: {...},
        validation: {...},
        research_gaps: {...},
        research_ideas: {...},
        summary: {...}
    }
```

### 3. Database Storage

```
save_research(query, agent_results)
    ↓
INSERT INTO research_queries (query, timestamp)
    ↓
For each agent:
    INSERT INTO research_results (query_id, agent_name, result_json)
```

### 4. Response → Frontend

```
Backend sends JSON response
    ↓
Frontend receives data
    ↓
displayResults(data.results)
    ↓
Render 6 sections with formatted cards
```

## Component Details

### Frontend Components

**index.html**
- Search input and button
- Loading spinner with progress steps
- Results container with 6 sections
- Error message display

**style.css**
- Gradient background
- Card-based layout
- Responsive design
- Animations and transitions

**script.js**
- Event handlers
- Fetch API calls
- Result rendering functions
- Error handling

### Backend Components

**app.py**
- Flask server setup
- CORS configuration
- Route handlers
- Error handling
- Database initialization

**Agents (7 modules)**
- Each agent is independent
- Processes input from previous agent
- Returns structured JSON
- Includes error handling and logging

**database/db.py**
- SQLite connection management
- CRUD operations
- Query functions
- Statistics

**services/arxiv_service.py**
- arXiv API integration
- XML parsing
- Error handling

## Technology Stack

### Frontend
```
HTML5
  └─ Semantic structure
  └─ Form elements
  └─ Section containers

CSS3
  └─ Flexbox/Grid layouts
  └─ Gradients and animations
  └─ Responsive design

JavaScript (ES6+)
  └─ Fetch API
  └─ DOM manipulation
  └─ Event handling
```

### Backend
```
Python 3.8+
  └─ Flask 3.0.0
      └─ REST API
      └─ JSON responses
      └─ Error handling
  └─ Flask-CORS 4.0.0
      └─ Cross-origin support
  └─ Requests 2.31.0
      └─ HTTP client
      └─ arXiv API calls
  └─ SQLite3
      └─ Built-in database
      └─ No external dependencies
```

## Agent Architecture

Each agent follows this pattern:

```python
class AgentName:
    def __init__(self):
        # Initialize agent-specific data
        pass
    
    def process(self, input_data):
        """
        Main processing method
        
        Args:
            input_data: Output from previous agent
            
        Returns:
            dict: Structured JSON output
        """
        try:
            # Process data
            result = self._process_logic(input_data)
            
            return {
                'agent': 'Agent Name',
                'status': 'completed',
                'data': result,
                'message': 'Success message'
            }
        except Exception as e:
            return {
                'agent': 'Agent Name',
                'status': 'error',
                'message': str(e)
            }
    
    def _process_logic(self, data):
        # Agent-specific processing
        pass
```

## API Endpoints

### Research Operations
```
POST   /api/research              # Process new query
GET    /api/research/<id>         # Get specific research
DELETE /api/research/<id>         # Delete research
GET    /api/research/<id>/agent/<name>  # Get agent result
```

### Query Management
```
GET    /api/queries               # List all queries
GET    /api/stats                 # Database statistics
```

### System
```
GET    /api/health                # Health check
GET    /api/agents                # List agents
```

## Database Schema

```sql
-- Research queries table
CREATE TABLE research_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Research results table
CREATE TABLE research_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_id INTEGER NOT NULL,
    agent_name TEXT NOT NULL,
    result_json TEXT NOT NULL,
    FOREIGN KEY (query_id) REFERENCES research_queries(id)
);

-- Indexes for performance
CREATE INDEX idx_query_id ON research_results(query_id);
CREATE INDEX idx_agent_name ON research_results(agent_name);
```

## Security Considerations

1. **Local Only**: Server runs on localhost (127.0.0.1)
2. **No Authentication**: Designed for single-user local use
3. **CORS Enabled**: Allows frontend to communicate with backend
4. **Input Validation**: Query validation before processing
5. **Error Handling**: Graceful error messages, no stack traces to user
6. **SQL Injection**: Protected by parameterized queries
7. **XSS Protection**: Text sanitization in frontend

## Performance Characteristics

### Processing Time
- Retrieval: 2-5 seconds (depends on arXiv API)
- Extraction: 1-2 seconds
- Comparison: 1 second
- Validation: 1 second
- Gap Analysis: 1 second
- Ideation: 1-2 seconds
- Output: <1 second

**Total: 10-30 seconds per query**

### Resource Usage
- Memory: ~50-100MB (backend)
- CPU: Low (mostly I/O bound)
- Storage: ~1MB per query (database)
- Network: ~500KB per query (arXiv API)

## Scalability Notes

### Current Limitations
- Single-threaded processing
- Sequential agent execution
- Local SQLite database
- No caching

### Potential Improvements
- Parallel agent execution
- Redis caching
- PostgreSQL for production
- Load balancing
- API rate limiting
- Background job queue

## Offline Capabilities

### Works Offline ✅
- Frontend interface
- Backend server
- Database operations
- Agent processing logic
- Result formatting

### Requires Internet ❌
- arXiv API calls
- Paper retrieval

### Hybrid Mode
The system can work in "offline mode" with cached data:
- Previous queries stored in database
- Can retrieve and display past results
- No new paper retrieval possible

## Error Handling Strategy

### Frontend
```javascript
try {
    const response = await fetch(...)
    if (!response.ok) throw new Error(...)
    // Process data
} catch (error) {
    showError(error.message)
}
```

### Backend
```python
try:
    # Process request
    result = process_data()
    return jsonify({'success': True, 'data': result})
except Exception as e:
    logger.error(f"Error: {str(e)}")
    return jsonify({'success': False, 'error': str(e)}), 500
```

### Agents
```python
try:
    # Agent logic
    return {'status': 'completed', ...}
except Exception as e:
    logger.error(f"Agent error: {str(e)}")
    return {'status': 'error', 'message': str(e)}
```

## Logging Strategy

All components use Python's logging module:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Processing started")
logger.warning("Potential issue detected")
logger.error("Error occurred")
```

## Future Architecture Enhancements

1. **Microservices**: Split agents into separate services
2. **Message Queue**: RabbitMQ/Celery for async processing
3. **Caching Layer**: Redis for API responses
4. **API Gateway**: Rate limiting and authentication
5. **Monitoring**: Prometheus + Grafana
6. **Containerization**: Docker deployment
7. **Cloud Ready**: AWS/GCP deployment options
8. **WebSockets**: Real-time progress updates

---

This architecture provides a solid foundation for a research analysis system that is:
- Easy to understand and maintain
- Modular and extensible
- Reliable with proper error handling
- Performant for local use
- Ready for future enhancements
