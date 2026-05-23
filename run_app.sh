#!/bin/bash
set -euo pipefail

# Always run from script directory
cd "$(dirname "$0")"

# ------------------
# Backend
# ------------------
cd backend

if [[ ! -d ".venv" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Starting backend..."
uvicorn main:app --reload &

# ------------------
# Frontend
# ------------------
cd ../frontend

if [[ ! -d "node_modules" ]]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "Starting frontend dev server..."
npm run dev
