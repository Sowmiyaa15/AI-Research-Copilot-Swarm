# AI Research Copilot Swarm

Multi-agent system for comprehensive research paper analysis using arXiv API.

## 🚀 Quick Start

### Windows
1. Double-click `RUN.bat` to start the backend
2. Double-click `OPEN_FRONTEND.bat` to open the dashboard
3. Enter your research query and click "Analyze Research"

### Linux/Mac
1. Run `chmod +x RUN.sh OPEN_FRONTEND.sh` (first time only)
2. Run `./RUN.sh` to start the backend
3. Run `./OPEN_FRONTEND.sh` to open the dashboard
4. Enter your research query and click "Analyze Research"

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start backend (keep this running)
cd backend
python app.py

# Open frontend/index.html in your browser
```

## 📋 Features

- 🔍 Automated paper retrieval from arXiv
- 🧠 Knowledge extraction from abstracts
- ⚖️ Method comparison and analysis
- ✅ Claim validation across papers
- 🔬 Research gap identification
- 💡 Research idea generation
- 📊 Beautiful dashboard interface
- 💾 SQLite database for storing results

## 🏗️ Architecture

The system uses 7 specialized agents that process research queries sequentially:

1. **Retrieval Agent** - Fetches top 5 papers from arXiv API
2. **Extraction Agent** - Extracts methods, findings, and problem domains
3. **Comparison Agent** - Compares methodologies and identifies strengths/weaknesses
4. **Validation Agent** - Validates consistency of claims across papers
5. **Gap Agent** - Identifies research gaps and opportunities
6. **Ideation Agent** - Generates actionable research ideas
7. **Output Agent** - Combines and formats all results

Each agent outputs structured JSON to the next agent in the pipeline.

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3 (with modern gradients and animations)
- Vanilla JavaScript (Fetch API)

### Backend
- Python 3.8+
- Flask (REST API)
- Flask-CORS (Cross-origin support)
- Requests (HTTP library)

### Database
- SQLite (for storing research queries and results)

### External APIs
- arXiv API (research paper retrieval)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser
- Internet connection (for arXiv API)

### Step-by-Step

1. **Install Dependencies**
```bash
cd ai_research_copilot
pip install -r requirements.txt
```

2. **Start Backend Server**
```bash
cd backend
python app.py
```
Backend runs on `http://localhost:5000`

3. **Open Frontend**
- Simply open `frontend/index.html` in your browser
- Or use Python HTTP server:
```bash
cd frontend
python -m http.server 8000
```
Then visit `http://localhost:8000`

4. **Use the Application**
- Enter a research query (e.g., "machine learning in healthcare")
- Click "Analyze Research"
- Wait 10-30 seconds for processing
- View results in 6 sections

## 📖 Usage

### Example Queries
- "deep learning for computer vision"
- "natural language processing transformers"
- "reinforcement learning robotics"
- "machine learning healthcare diagnosis"
- "neural architecture search"

### Dashboard Sections

1. **Executive Summary** - Overview statistics and key insights
2. **Retrieved Papers** - Top 5 papers from arXiv with abstracts
3. **Knowledge Extraction** - Methods, findings, and problem domains
4. **Method Comparison** - Strengths, weaknesses, best performing method
5. **Claim Validation** - Consistent and conflicting claims with confidence score
6. **Research Gaps** - Identified opportunities categorized by type
7. **Research Ideas** - Actionable proposals with impact and feasibility ratings

## 🔌 API Endpoints

### Research Analysis
- `POST /api/research` - Process research query
- `GET /api/research/<id>` - Retrieve specific research
- `DELETE /api/research/<id>` - Delete research

### Query Management
- `GET /api/queries` - List all queries
- `GET /api/research/<id>/agent/<name>` - Get specific agent result

### System
- `GET /api/health` - Health check
- `GET /api/agents` - List all agents
- `GET /api/stats` - Database statistics

## 📁 Project Structure

```
ai_research_copilot/
├── backend/
│   ├── app.py                 # Flask application
│   ├── agents/
│   │   ├── retrieval_agent.py
│   │   ├── extraction_agent.py
│   │   ├── comparison_agent.py
│   │   ├── validation_agent.py
│   │   ├── gap_agent.py
│   │   ├── ideation_agent.py
│   │   └── output_agent.py
│   ├── services/
│   │   └── arxiv_service.py   # arXiv API integration
│   ├── database/
│   │   └── db.py              # SQLite database
│   └── models/
│       └── research.py        # Data models
├── frontend/
│   ├── index.html             # Main dashboard
│   ├── style.css              # Styling
│   └── script.js              # Frontend logic
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── SETUP.md                   # Detailed setup guide
├── RUN.bat                    # Windows launcher
├── RUN.sh                     # Linux/Mac launcher
├── OPEN_FRONTEND.bat          # Windows frontend opener
└── OPEN_FRONTEND.sh           # Linux/Mac frontend opener
```

## 🌐 Offline Capabilities

✅ **Works Offline:**
- Frontend (HTML, CSS, JavaScript)
- Backend server (Flask)
- Database (SQLite)
- All 7 agents (processing logic)
- Results display and formatting

❌ **Requires Internet:**
- arXiv API calls (retrieving research papers)

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed: `python --version`
- Check if port 5000 is available
- Verify dependencies: `pip install -r requirements.txt`

### CORS errors
- Ensure Flask-CORS is installed
- Restart backend server
- Clear browser cache

### No papers retrieved
- Check internet connection
- Verify arXiv API is accessible
- Try a different/broader query

### Frontend not connecting
- Verify backend is running on localhost:5000
- Check browser console (F12) for errors
- Test health endpoint: `http://localhost:5000/api/health`

See `SETUP.md` for detailed troubleshooting guide.

## 📊 Database Schema

### research_queries
- `id` - Primary key
- `query` - Research query text
- `timestamp` - When query was made

### research_results
- `id` - Primary key
- `query_id` - Foreign key to research_queries
- `agent_name` - Name of the agent
- `result_json` - JSON result from agent

## 🔒 Security Notes

- Backend runs on localhost only (not exposed to internet)
- No authentication required (local use only)
- Database stored locally
- No data sent to external services (except arXiv API)

## 🚀 Future Enhancements

- Support for multiple research databases (PubMed, IEEE, etc.)
- User authentication and saved queries
- Export results to PDF/Word
- Advanced filtering and sorting
- Citation network analysis
- Collaborative features
- Real-time collaboration
- Cloud deployment option

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For detailed setup instructions, see `SETUP.md`

For issues and questions, check the troubleshooting section above.

---

**Powered by arXiv API | 7 Specialized AI Agents | Built with Flask & Vanilla JS**
