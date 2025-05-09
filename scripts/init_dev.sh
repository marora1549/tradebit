#!/bin/bash

# Initialize development environment for TradeBit

# Exit on error
set -e

echo "TradeBit Development Environment Setup"
echo "--------------------------------------"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "Warning: PostgreSQL command line tools not found. You may need to install PostgreSQL."
fi

# Check if Node.js and npm are installed
if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
    echo "Warning: Node.js or npm not found. You may need to install Node.js and npm."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit the .env file with your database settings."
fi

# Create database if it doesn't exist and PostgreSQL is available
if command -v psql &> /dev/null; then
    DB_NAME=$(grep DB_NAME .env | cut -d '=' -f2)
    DB_USER=$(grep DB_USER .env | cut -d '=' -f2)
    
    if [ -n "$DB_NAME" ] && [ -n "$DB_USER" ]; then
        echo "Checking if database '$DB_NAME' exists..."
        if ! psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
            echo "Creating database '$DB_NAME'..."
            createdb "$DB_NAME"
        else
            echo "Database '$DB_NAME' already exists."
        fi
    else
        echo "Warning: Database name or user not found in .env file."
    fi
fi

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Prompt to create superuser
echo "Do you want to create a superuser? (y/n)"
read CREATE_SUPERUSER
if [ "$CREATE_SUPERUSER" = "y" ]; then
    python manage.py createsuperuser
fi

# Install frontend dependencies
if [ -d "frontend" ]; then
    echo "Installing frontend dependencies..."
    cd frontend
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        echo "Creating frontend .env file..."
        cp .env.example .env
    fi
    
    npm install
    cd ..
fi

echo "\nSetup complete! You can now start the development servers:\n"
echo "Backend:  python manage.py runserver"
echo "Frontend: cd frontend && npm start"
echo "\nOr use Docker Compose: docker-compose up\n"
