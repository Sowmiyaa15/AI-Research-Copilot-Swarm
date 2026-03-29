#!/bin/bash

echo "========================================"
echo "AI Research Copilot Swarm - Linux/Mac"
echo "========================================"
echo ""

echo "Step 1: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi
python3 --version
echo ""

echo "Step 2: Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

echo "Step 3: Starting backend server..."
echo "Backend will run on http://localhost:5000"
echo ""
echo "IMPORTANT: Keep this terminal open!"
echo ""
echo "To stop the server, press Ctrl+C"
echo ""
echo "========================================"
echo "Starting in 3 seconds..."
sleep 3

cd backend
python3 app.py
