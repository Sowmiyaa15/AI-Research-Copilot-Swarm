#!/bin/bash

echo "Opening AI Research Copilot Swarm frontend..."
echo ""
echo "Make sure the backend server is running!"
echo "If not, run ./RUN.sh first."
echo ""
sleep 2

cd frontend

# Try to open with default browser
if command -v xdg-open &> /dev/null; then
    xdg-open index.html
elif command -v open &> /dev/null; then
    open index.html
else
    echo "Please open frontend/index.html manually in your browser"
fi
