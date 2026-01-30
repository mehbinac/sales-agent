#!/bin/bash
# Start the E-commerce Sales Agent Streamlit frontend

echo "Starting E-commerce Sales Agent Frontend..."
echo "The frontend will be available at http://localhost:8501"
echo ""
echo "Make sure the API is running at http://localhost:8000"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Start the frontend
streamlit run frontend/streamlit_app.py --server.port 8501
