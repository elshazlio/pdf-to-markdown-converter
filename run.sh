#!/bin/bash

# PDF to Markdown Converter - Launch Script
# This script activates the virtual environment and runs the Streamlit app

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Setting up for the first time..."
    echo ""
    
    # Create virtual environment
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    
    # Activate and install dependencies
    echo "📥 Installing dependencies..."
    source venv/bin/activate
    pip install -q -r requirements.txt
    
    echo "✅ Setup complete!"
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Run Streamlit app
echo "🚀 Starting PDF to Markdown Converter..."
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py

