#!/bin/bash
# Start the E-commerce Sales Agent API server

echo "Starting E-commerce Sales Agent API..."
echo "The API will be available at http://localhost:8000"
echo "API Documentation will be at http://localhost:8000/docs"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Start the server
python -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
