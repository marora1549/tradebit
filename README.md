# TradeBit

## Personal Stock Portfolio Management System

TradeBit is a comprehensive Django-based personal stock portfolio management system that integrates with Zerodha Kite API. It provides a seamless experience for tracking, analyzing, and managing your stock investments.

![TradeBit Dashboard](docs/images/dashboard.png)

## Key Features

- **Portfolio Tracking**: Monitor your holdings, purchase history, and performance metrics
- **Zerodha Integration**: Connect directly to your Zerodha account to sync holdings and place orders
- **Custom Classifications**: Organize your investments with customizable classifications
- **Performance Analytics**: Visualize your portfolio performance with detailed charts and metrics
- **Secure Authentication**: JWT-based authentication system for secure access

## Technology Stack

### Backend
- Django with Django REST Framework
- PostgreSQL database
- JWT authentication

### Frontend
- React with TypeScript
- Tailwind CSS with shadcn/ui components
- React Query for data fetching
- Recharts for visualizations

### DevOps
- Docker and Docker Compose
- Nginx for production deployment
- Let's Encrypt for SSL

## Project Structure

The project is organized into several Django apps:
- `core`: Shared models, utilities, and common functionality
- `portfolio`: Holdings management and portfolio analysis
- `users`: User authentication and profile management
- `zerodha`: Integration with Zerodha Kite API

## Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL
- Node.js and npm
- Docker and Docker Compose (optional)

### Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tradebit.git
   cd tradebit
   ```

2. Start the development environment:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Backend: http://localhost:8000/api/v1/
   - Frontend: http://localhost:3000/
   - Admin: http://localhost:8000/admin/

### Manual Setup

See the [Setup Guide](docs/setup.md) for detailed instructions on manual setup for development and production.

## Documentation

- [Setup Guide](docs/setup.md)
- [API Documentation](docs/api.md)
- [Database Schema](docs/schema.md)
- [Frontend Architecture](docs/frontend.md)

## Development

### Helper Scripts

The repository includes helper scripts for development and deployment:

- `scripts/init_dev.sh`: Initialize the development environment
- `scripts/deploy.sh`: Deploy the application to a production server

### Running Tests

```bash
# Backend tests
python manage.py test

# Frontend tests
cd frontend
npm test
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is available under the MIT License.
