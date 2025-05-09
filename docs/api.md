# TradeBit API Documentation

This document provides detailed information about the TradeBit API endpoints.

## Authentication

TradeBit uses JWT (JSON Web Token) for authentication. You need to include the token in the Authorization header of your requests.

```
Authorization: Bearer <your_token>
```

### Obtaining a Token

**Endpoint**: `/api/v1/token/`

**Method**: POST

**Request Body**:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response**:
```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```

### Refreshing a Token

**Endpoint**: `/api/v1/token/refresh/`

**Method**: POST

**Request Body**:
```json
{
  "refresh": "your_refresh_token"
}
```

**Response**:
```json
{
  "access": "your_new_access_token"
}
```

## User Management

### Register a New User

**Endpoint**: `/api/v1/users/register/`

**Method**: POST

**Request Body**:
```json
{
  "username": "new_user",
  "email": "user@example.com",
  "password": "secure_password",
  "password2": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response**:
```json
{
  "id": 1,
  "username": "new_user",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Get User Profile

**Endpoint**: `/api/v1/users/profile/`

**Method**: GET

**Response**:
```json
{
  "id": 1,
  "username": "new_user",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": null,
  "profile_image": null
}
```

### Update User Profile

**Endpoint**: `/api/v1/users/profile/`

**Method**: PATCH

**Request Body**:
```json
{
  "first_name": "Updated",
  "last_name": "Name",
  "bio": "This is my bio"
}
```

**Response**:
```json
{
  "id": 1,
  "username": "new_user",
  "email": "user@example.com",
  "first_name": "Updated",
  "last_name": "Name",
  "bio": "This is my bio",
  "profile_image": null
}
```

### Change Password

**Endpoint**: `/api/v1/users/change-password/`

**Method**: POST

**Request Body**:
```json
{
  "old_password": "current_password",
  "new_password": "new_secure_password",
  "new_password2": "new_secure_password"
}
```

**Response**:
```json
{
  "message": "Password updated successfully."
}
```

### Get User Settings

**Endpoint**: `/api/v1/users/settings/`

**Method**: GET

**Response**:
```json
{
  "id": 1,
  "theme": "system",
  "default_view": "portfolio",
  "notifications_enabled": true,
  "email_notifications": true,
  "user_details": {
    "id": 1,
    "username": "new_user",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": null,
    "profile_image": null
  }
}
```

### Update User Settings

**Endpoint**: `/api/v1/users/settings/`

**Method**: PATCH

**Request Body**:
```json
{
  "theme": "dark",
  "default_view": "analytics",
  "notifications_enabled": false,
  "email_notifications": false
}
```

**Response**:
```json
{
  "id": 1,
  "theme": "dark",
  "default_view": "analytics",
  "notifications_enabled": false,
  "email_notifications": false,
  "user_details": {
    "id": 1,
    "username": "new_user",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": null,
    "profile_image": null
  }
}
```

### Update Zerodha Credentials

**Endpoint**: `/api/v1/users/zerodha-credentials/`

**Method**: POST

**Request Body**:
```json
{
  "api_key": "your_zerodha_api_key",
  "api_secret": "your_zerodha_api_secret"
}
```

**Response**:
```json
{
  "message": "Zerodha credentials updated successfully."
}
```

## Core Resources

### List Stocks

**Endpoint**: `/api/v1/core/stocks/`

**Method**: GET

**Query Parameters**:
- `sector`: Filter by sector
- `industry`: Filter by industry
- `is_active`: Filter by active status (true/false)
- `search`: Search in symbol and name fields
- `ordering`: Order by field (e.g. symbol, name, sector, industry)

**Response**:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/core/stocks/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "symbol": "RELIANCE",
      "name": "Reliance Industries Ltd.",
      "sector": "Energy",
      "industry": "Oil & Gas",
      "is_active": true
    },
    // More stocks...
  ]
}
```

### Create Stock

**Endpoint**: `/api/v1/core/stocks/`

**Method**: POST

**Request Body**:
```json
{
  "symbol": "TCS",
  "name": "Tata Consultancy Services",
  "sector": "Technology",
  "industry": "IT Services",
  "is_active": true
}
```

**Response**:
```json
{
  "id": 2,
  "symbol": "TCS",
  "name": "Tata Consultancy Services",
  "sector": "Technology",
  "industry": "IT Services",
  "is_active": true
}
```

### List Stock Aliases

**Endpoint**: `/api/v1/core/stock-aliases/`

**Method**: GET

**Query Parameters**:
- `stock`: Filter by stock ID
- `search`: Search in alias, stock__symbol, or stock__name fields

**Response**:
```json
{
  "count": 50,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "stock": 1,
      "alias": "Reliance",
      "stock_details": {
        "id": 1,
        "symbol": "RELIANCE",
        "name": "Reliance Industries Ltd.",
        "sector": "Energy",
        "industry": "Oil & Gas",
        "is_active": true
      }
    },
    // More aliases...
  ]
}
```

### List Classifications

**Endpoint**: `/api/v1/core/classifications/`

**Method**: GET

**Query Parameters**:
- `type`: Filter by classification type
- `search`: Search in name, type, or description fields
- `ordering`: Order by field (e.g. name, type)

**Response**:
```json
{
  "count": 30,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Long Term",
      "type": "Investment Horizon",
      "description": "Investments intended to be held for 3+ years"
    },
    // More classifications...
  ]
}
```

## Portfolio Management

### List Holdings

**Endpoint**: `/api/v1/portfolio/holdings/`

**Method**: GET

**Query Parameters**:
- `stock`: Filter by stock ID
- `source`: Filter by source (e.g. manual, zerodha)
- `search`: Search in stock__symbol, stock__name, or notes fields
- `ordering`: Order by field (e.g. purchase_date, quantity, avg_price)

**Response**:
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "stock": 1,
      "quantity": "10.0000",
      "avg_price": "2000.00",
      "purchase_date": "2023-05-01",
      "notes": null,
      "source": "manual",
      "external_id": null,
      "total_value": "20000.00",
      "stock_details": {
        "id": 1,
        "symbol": "RELIANCE",
        "name": "Reliance Industries Ltd.",
        "sector": "Energy",
        "industry": "Oil & Gas",
        "is_active": true
      },
      "user_details": {
        "id": 1,
        "username": "new_user",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "bio": null,
        "profile_image": null
      },
      "created_at": "2023-05-01T10:00:00Z",
      "updated_at": "2023-05-01T10:00:00Z"
    },
    // More holdings...
  ]
}
```

### Create Holding

**Endpoint**: `/api/v1/portfolio/holdings/`

**Method**: POST

**Request Body**:
```json
{
  "stock": 1,
  "quantity": "5.0000",
  "avg_price": "1950.00",
  "purchase_date": "2023-06-15",
  "notes": "Added to portfolio",
  "source": "manual"
}
```

**Response**:
```json
{
  "id": 2,
  "user": 1,
  "stock": 1,
  "quantity": "5.0000",
  "avg_price": "1950.00",
  "purchase_date": "2023-06-15",
  "notes": "Added to portfolio",
  "source": "manual",
  "external_id": null,
  "total_value": "9750.00",
  "stock_details": {
    "id": 1,
    "symbol": "RELIANCE",
    "name": "Reliance Industries Ltd.",
    "sector": "Energy",
    "industry": "Oil & Gas",
    "is_active": true
  },
  "user_details": {
    "id": 1,
    "username": "new_user",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": null,
    "profile_image": null
  },
  "created_at": "2023-06-15T14:30:00Z",
  "updated_at": "2023-06-15T14:30:00Z"
}
```

### Get Portfolio Summary

**Endpoint**: `/api/v1/portfolio/summary/`

**Method**: GET

**Response**:
```json
{
  "total_value": "29750.00",
  "total_holdings": 2,
  "sectors": {
    "Energy": "29750.00",
    "Technology": "0.00"
  },
  "top_holdings": [
    {
      "id": 1,
      "stock_details": {
        "symbol": "RELIANCE",
        "name": "Reliance Industries Ltd."
      },
      "quantity": "10.0000",
      "avg_price": "2000.00",
      "total_value": "20000.00"
    },
    {
      "id": 2,
      "stock_details": {
        "symbol": "RELIANCE",
        "name": "Reliance Industries Ltd."
      },
      "quantity": "5.0000",
      "avg_price": "1950.00",
      "total_value": "9750.00"
    }
  ]
}
```

## Zerodha Integration

### Get Zerodha Login URL

**Endpoint**: `/api/v1/zerodha/login/`

**Method**: GET

**Response**:
```json
{
  "login_url": "https://kite.zerodha.com/connect/login?api_key=your_api_key&v=3"
}
```

### Handle Zerodha Callback

**Endpoint**: `/api/v1/zerodha/callback/`

**Method**: GET

**Query Parameters**:
- `request_token`: The request token from Zerodha

**Response**:
```json
{
  "success": true,
  "message": "Zerodha authentication successful"
}
```

### Get Zerodha Holdings

**Endpoint**: `/api/v1/zerodha/holdings/`

**Method**: GET

**Response**:
```json
[
  {
    "tradingsymbol": "RELIANCE",
    "exchange": "NSE",
    "isin": "INE002A01018",
    "quantity": 15,
    "average_price": 1983.33,
    "last_price": 2100.50,
    "pnl": 1757.55,
    "day_change": 25.5,
    "day_change_percentage": 1.23,
    "product": "CNC"
  },
  // More holdings...
]
```

### Sync Zerodha Holdings

**Endpoint**: `/api/v1/zerodha/sync-holdings/`

**Method**: POST

**Response**:
```json
{
  "success": true,
  "created": 2,
  "updated": 1,
  "skipped": 0,
  "total": 3
}
```

### Get Zerodha Orders

**Endpoint**: `/api/v1/zerodha/orders/`

**Method**: GET

**Response**:
```json
[
  {
    "order_id": "123456789",
    "exchange": "NSE",
    "tradingsymbol": "RELIANCE",
    "transaction_type": "BUY",
    "order_type": "MARKET",
    "quantity": 5,
    "price": null,
    "status": "COMPLETE",
    "filled_quantity": 5,
    "pending_quantity": 0,
    "average_price": 1950.75
  },
  // More orders...
]
```

### Place Zerodha Order

**Endpoint**: `/api/v1/zerodha/place-order/`

**Method**: POST

**Request Body**:
```json
{
  "exchange": "NSE",
  "tradingsymbol": "RELIANCE",
  "transaction_type": "BUY",
  "quantity": 1,
  "product": "CNC",
  "order_type": "MARKET"
}
```

**Response**:
```json
{
  "success": true,
  "order_id": "987654321",
  "message": "Order placed successfully"
}
```
