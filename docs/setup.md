# TradeBit - Setup Guide

This guide will help you set up TradeBit for development and deployment.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
   - [Backend Setup](#backend-setup)
   - [Frontend Setup](#frontend-setup)
3. [Docker Development](#docker-development)
4. [Production Deployment](#production-deployment)
5. [Zerodha Integration](#zerodha-integration)

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.11 or higher
- PostgreSQL 13 or higher
- Node.js 18 or higher and npm
- Docker and Docker Compose (for containerized setup)

## Local Development

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tradebit.git
   cd tradebit
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file by copying the example:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file to configure your database settings and other variables.

6. Create the database:
   ```bash
   createdb tradebit  # If using PostgreSQL command line
   ```

7. Apply migrations:
   ```bash
   python manage.py migrate
   ```

8. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

9. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file to configure your API URL and other variables.

5. Start the development server:
   ```bash
   npm start
   ```

## Docker Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tradebit.git
   cd tradebit
   ```

2. Create a `.env` file by copying the example:
   ```bash
   cp .env.example .env
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. Create a superuser (in a separate terminal):
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

5. Access the application:
   - Backend: http://localhost:8000/api/v1/
   - Frontend: http://localhost:3000/
   - Admin: http://localhost:8000/admin/

## Production Deployment

1. Clone the repository on your production server:
   ```bash
   git clone https://github.com/yourusername/tradebit.git
   cd tradebit
   ```

2. Create a `.env` file with production settings:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file with your production settings, including:
   - Set `DEBUG=False`
   - Set a strong `SECRET_KEY`
   - Configure your database settings
   - Set `ALLOWED_HOSTS` to your domain(s)
   - Configure email settings

4. Edit `nginx/prod.conf` to use your domain name instead of `yourdomain.com`.

5. Build and start the production containers:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

6. Initialize SSL certificates with Let's Encrypt:
   ```bash
   docker-compose -f docker-compose.prod.yml exec certbot certbot certonly --webroot -w /var/www/certbot -d yourdomain.com -d www.yourdomain.com
   ```

7. Create a superuser:
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
   ```

## Zerodha Integration

To integrate with Zerodha Kite API, follow these steps:

1. Sign up for a [Zerodha Developer Account](https://developers.kite.trade/).

2. Create a new application and note your API Key and Secret.

3. Configure your redirect URL in the Zerodha Developer Console:
   - For development: `http://localhost:3000/zerodha`
   - For production: `https://yourdomain.com/zerodha`

4. Update your settings via the TradeBit user interface:
   - Log in to your TradeBit account
   - Go to Settings
   - Enter your Zerodha API Key and Secret

5. Connect your account:
   - Go to the Zerodha Integration page
   - Click "Connect with Zerodha"
   - Complete the authorization process

6. Sync your holdings:
   - After connecting, click "Sync Holdings" to import your holdings from Zerodha

## Additional Resources

- [API Documentation](api.md)
- [Database Schema](schema.md)
- [Frontend Architecture](frontend.md)
