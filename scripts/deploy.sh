#!/bin/bash

# Deployment script for TradeBit

# Exit on error
set -e

echo "TradeBit Deployment Script"
echo "------------------------"

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker and Docker Compose are required for deployment. Please install them and try again."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit the .env file with your production settings."
    exit 1
fi

# Prompt for domain name
echo "Enter your domain name (e.g., example.com):"
read DOMAIN_NAME

if [ -z "$DOMAIN_NAME" ]; then
    echo "Error: Domain name is required."
    exit 1
fi

# Update nginx configuration with the domain name
echo "Updating nginx configuration..."
sed -i "s/yourdomain\.com/$DOMAIN_NAME/g" nginx/prod.conf

# Pull latest changes
echo "Pulling latest changes..."
git pull

# Build and start containers
echo "Building and starting containers..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Initialize SSL certificates with Let's Encrypt
echo "Initializing SSL certificates..."
docker-compose -f docker-compose.prod.yml exec certbot certbot certonly --webroot -w /var/www/certbot -d $DOMAIN_NAME -d www.$DOMAIN_NAME

# Apply migrations
echo "Applying migrations..."
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Collect static files
echo "Collecting static files..."
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput

# Prompt to create superuser
echo "Do you want to create a superuser? (y/n)"
read CREATE_SUPERUSER
if [ "$CREATE_SUPERUSER" = "y" ]; then
    docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
fi

# Restart nginx to apply SSL configuration
echo "Restarting nginx..."
docker-compose -f docker-compose.prod.yml restart nginx

echo "\nDeployment complete! Your application should be available at https://$DOMAIN_NAME\n"
