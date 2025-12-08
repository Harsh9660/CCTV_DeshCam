#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting CCTV Dashcam System...${NC}"

# Function to kill background processes on exit
cleanup() {
    echo -e "${BLUE}Shutting down services...${NC}"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

trap cleanup SIGINT

# Activate Virtual Environment
if [ -d "env" ]; then
    echo -e "${GREEN}Activating virtual environment...${NC}"
    source env/bin/activate
else
    echo "Virtual environment not found. Please create one named 'env'."
    exit 1
fi

# Start Backend
echo -e "${GREEN}Starting Backend Server...${NC}"
cd Backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Start Frontend
echo -e "${GREEN}Starting Frontend Dashboard...${NC}"
cd Frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "${BLUE}System is running! Access the dashboard at the URL shown above.${NC}"
echo -e "${BLUE}Press Ctrl+C to stop.${NC}"

wait
