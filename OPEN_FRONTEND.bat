@echo off
echo Opening AI Research Copilot Swarm frontend...
echo.
echo Make sure the backend server is running!
echo If not, run RUN.bat first.
echo.
timeout /t 2 /nobreak > nul

cd frontend
start index.html
