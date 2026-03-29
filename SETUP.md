# AI Research Copilot Swarm - Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection (only for arXiv API calls)

## Quick Start Guide

### Step 1: Install Dependencies

Open your terminal/command prompt and navigate to the project directory:

```bash
cd ai_research_copilot
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-3.0.0 flask-cors-4.0.0 requests-2.31.0
```

### Step 2: Start the Backend Server

```bash
cd backend
python app.py
```

**Expected output:**
```
INFO:__main__:Starting AI Research Copilot Swarm backend server
INFO:__main__:Server running on http://localhost:5000
INFO:__main__:API endpoint: POST http://localhost:5000/api/research
 * Running on http://0.0.0.0:5000
```

**Keep this terminal window open!** The server must remain running.

### Step 3: Open the Frontend

**Option A: Direct File Access**
1. Navigate to the `frontend` folder
2. Double-click `index.html`
3. It will open in your default browser

**Option B: Using Python HTTP Server (Recommended)**

Open a NEW terminal window:

```bash
cd ai_research_copilot/frontend
python -m http.server 8000
```

Then open your browser and go to: `http://localhost:8000`

### Step 4: Enter Research Topic

1. In the input box, type your research query
   - Example: "machine learning in healthcare"
   - Example: "deep learning computer vision"
   - Example: "natural language processing transformers"

2. Click the "🔍 Analyze Research" button

3. Wait 10-30 seconds while the 7 agents process your query

### Step 5: View All Agent Outputs

The dashboard will display 6 sections with formatted cards:

1. **📊 Executive Summary** - Overview statistics and key insights
2. **📚 Retrieved Papers** - Top 5 papers from arXiv
3. **🔬 Knowledge Extraction** - Methods, findings, and domains
4. **⚖️ Method Comparison** - Strengths, weaknesses, best performing
5. **✅ Claim Validation** - Consistent and conflicting claims
6. **🔍 Research Gaps** - Identified opportunities
7. **💡 Research Ideas** - Actionable research proposals

## Offline Capabilities

✅ **Works Offline:**
- Frontend (HTML, CSS, JavaScript)
- Backend server (Flask)
- Database (SQLite)
- All 7 agents (processing logic)
- Results display and formatting

❌ **Requires Internet:**
- arXiv API calls (retrieving research papers)

## Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"

**Solution:**
Edit `backend/app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed from 5000
```

Then update `frontend/script.js`:
```javascript
const API_URL = 'http://localhost:5001/api';  // Changed from 5000
```

### Issue: CORS errors in browser console

**Solution:**
1. Make sure Flask-CORS is installed: `pip install flask-cors`
2. Restart the backend server
3. Clear browser cache (Ctrl+Shift+Delete)

### Issue: "No papers retrieved"

**Possible causes:**
- No internet connection
- arXiv API is down
- Query is too specific

**Solution:**
- Check internet connection
- Try a broader query
- Wait a few minutes and try again

### Issue: Frontend not connecting to backend

**Solution:**
1. Verify backend is running (check terminal)
2. Check URL is correct: `http://localhost:5000`
3. Open browser console (F12) to see error messages
4. Try accessing health endpoint: `http://localhost:5000/api/health`

## Testing the Installation

### Test 1: Backend Health Check

Open browser and visit: `http://localhost:5000/api/health`

**Expected response:**
```json
{
  "status": "ok",
  "service": "AI Research Copilot Swarm",
  "version": "1.0.0",
  "agents": [...]
}
```

### Test 2: Database Stats

Visit: `http://localhost:5000/api/stats`

**Expected response:**
```json
{
  "success": true,
  "stats": {
    "total_queries": 0,
    "total_results": 0,
    ...
  }
}
```

### Test 3: Run Sample Query

Use this curl command or Postman:

```bash
curl -X POST http://localhost:5000/api/research \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning"}'
```

## Database Location

The SQLite database is created at:
```
ai_research_copilot/backend/research.db
```

You can view it with any SQLite browser tool.

## Stopping the Application

1. **Stop Backend:** Press `Ctrl+C` in the terminal running the backend
2. **Stop Frontend Server (if using):** Press `Ctrl+C` in the frontend terminal
3. **Close Browser:** Simply close the browser tab

## Advanced Usage

### View Previous Queries

Visit: `http://localhost:5000/api/queries`

### Retrieve Specific Research

Visit: `http://localhost:5000/api/research/<query_id>`

Example: `http://localhost:5000/api/research/1`

### Delete Research

```bash
curl -X DELETE http://localhost:5000/api/research/1
```

## System Requirements

**Minimum:**
- CPU: Dual-core processor
- RAM: 2GB
- Storage: 100MB
- Internet: Required for arXiv API

**Recommended:**
- CPU: Quad-core processor
- RAM: 4GB+
- Storage: 500MB
- Internet: Broadband connection

## Performance Notes

- First query may take 15-30 seconds
- Subsequent queries: 10-20 seconds
- Processing time depends on:
  - Number of papers retrieved
  - Internet speed
  - System resources

## Security Notes

- Backend runs on localhost only (not exposed to internet)
- No authentication required (local use only)
- Database stored locally
- No data sent to external services (except arXiv API)

## Next Steps

After successful setup:

1. Try different research queries
2. Explore the 6 result sections
3. Review research ideas generated
4. Check database stats
5. View previous queries

## Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review terminal output for error messages
3. Check browser console (F12) for frontend errors
4. Verify all dependencies are installed
5. Ensure Python version is 3.8+

## File Structure

```
ai_research_copilot/
├── backend/
│   ├── app.py              # Flask server (must be running)
│   ├── agents/             # 7 agent modules
│   ├── services/           # arXiv API service
│   ├── database/           # SQLite database
│   └── research.db         # Database file (created on first run)
├── frontend/
│   ├── index.html          # Main dashboard
│   ├── style.css           # Styling
│   └── script.js           # Frontend logic
├── requirements.txt        # Python dependencies
├── README.md              # Project overview
└── SETUP.md               # This file
```

## Success Indicators

✅ Backend running without errors
✅ Frontend loads in browser
✅ Can enter research query
✅ Progress indicators show during processing
✅ All 6 sections display results
✅ Papers retrieved from arXiv
✅ Research ideas generated

Enjoy using AI Research Copilot Swarm! 🚀
