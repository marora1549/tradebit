# TradeBit Database Schema

This document outlines the database schema for the TradeBit application.

## Overview

TradeBit uses a PostgreSQL database with the following key models:

- **User**: Custom user model extending Django's AbstractUser
- **Stock**: Represents a stock in the market
- **StockAlias**: Alternative names/symbols for stocks
- **Holding**: User's stock holdings
- **Classification**: Custom classifications for holdings
- **HoldingClass**: Mapping between holdings and classifications
- **UserSettings**: User-specific settings and preferences

## Entity Relationship Diagram

```
┌───────────────────┐           ┌──────────────────┐
│        User       │           │   UserSettings   │
├───────────────────┤           ├──────────────────┤
│ id                │◄─────────►│ user             │
│ username          │           │ theme            │
│ email             │           │ default_view     │
│ password          │           │ zerodha_api_key  │
│ first_name        │           │ zerodha_api_secret│
│ last_name         │           │ ...              │
│ bio               │           └──────────────────┘
│ profile_image     │                    ▲
└───────────────────┘                    │
          ▲                              │
          │                              │
          │                              │
┌───────────────────┐           ┌──────────────────┐
│      Holding      │           │    HoldingClass  │
├───────────────────┤           ├──────────────────┤
│ id                │◄─────────►│ holding          │
│ user              │           │ classification    │
│ stock             │           └──────────────────┘
│ quantity          │                    ▲
│ avg_price         │                    │
│ purchase_date     │                    │
│ notes             │           ┌──────────────────┐
│ source            │           │  Classification  │
│ external_id       │           ├──────────────────┤
└───────────────────┘           │ id               │
          ▲                     │ name             │
          │                     │ type             │
          │                     │ description      │
┌───────────────────┐           └──────────────────┘
│       Stock       │
├───────────────────┤
│ id                │
│ symbol            │
│ name              │
│ sector            │
│ industry          │
│ is_active         │
└───────────────────┘
          ▲
          │
          │
┌───────────────────┐
│     StockAlias    │
├───────────────────┤
│ id                │
│ stock             │
│ alias             │
└───────────────────┘
```

## Model Details

### User

Extends Django's AbstractUser model with additional fields.

| Field | Type | Description |
|-------|------|-------------|
| id | BigAutoField | Primary key |
| username | CharField | Unique username |
| email | EmailField | Unique email address |
| password | CharField | Hashed password |
| first_name | CharField | First name |
| last_name | CharField | Last name |
| bio | TextField | Optional biography |
| profile_image | ImageField | Optional profile image |
| created_at | DateTimeField | Timestamp when user was created |
| updated_at | DateTimeField | Timestamp when user was last updated |

### UserSettings

Stores user-specific settings and preferences.

| Field | Type | Description |
|-------|------|-------------|
| id | BigAutoField | Primary key |
| user | OneToOneField | User associated with these settings |
| theme | CharField | UI theme preference (light, dark, system) |
| default_view | CharField | Default view (portfolio, watchlist, analytics) |
| zerodha_api_key | CharField | Zerodha API key |
| zerodha_api_secret | CharField | Zerodha API secret |
| zerodha_request_token | CharField | Zerodha request token for authentication |
| zerodha_access_token | CharField | Zerodha access token |
| zerodha_refresh_token | CharField | Zerodha refresh token |
| zerodha_session_expiry | DateTimeField | Expiry time for Zerodha session |
| notifications_enabled | BooleanField | Whether notifications are enabled |
| email_notifications | BooleanField | Whether email notifications are enabled |
| created_at | DateTimeField | Timestamp when settings were created |
| updated_at | DateTimeField | Timestamp when settings were last updated |

### Stock

Represents a stock in the market.

| Field | Type | Description |
|-------|------|-------------|
| id | BigAutoField | Primary key |
| symbol | CharField | Unique stock symbol |
| name | CharField | Company name |
| sector | CharField | Industry sector |
| industry | CharField | Specific industry |
| is_active | BooleanField | Whether the stock is active |
| created_at | DateTimeField | Timestamp when stock was created |
| updated_at | DateTimeField | Timestamp when stock was last updated |

### StockAlias

Alternative names/symbols for a stock.

| Field | Type | Description |
|-------|------|-------------|
| id | BigAutoField | Primary key |
| stock | ForeignKey | Associated stock |
| alias | CharField | Alternative name or symbol |
| created_at | DateTimeField | Timestamp when alias was created |
| updated_at | DateTimeField | Timestamp when alias was last updated |

### Holding

Represents a stock holding in a user's portfolio.

| Field | Type | Description |
|-------|------|-------------|
| id | BigAutoField | Primary key |
| user | ForeignKey | User who owns the holding |
| stock | ForeignKey | Associated stock |
| quantity | DecimalField | Quantity of shares |
| avg_price | DecimalField | Average purchase price |
| purchase_date | DateField | Date of purchase |
| notes | TextField | Optional notes |
| source | CharField | Source of the holding data (e.g., manual, zerodha) |
| external_id | CharField | ID used by external system if imported |
| created_at | DateTimeField | Timestamp when holding was created |
| updated_at | DateTimeField | Timestamp when holding was last updated |

### Classification

Custom classification for holdings.

| Field | Type | Description |
|-------|------|-------------|
| id | BigAutoField | Primary key |
| name | CharField | Classification name |
| type | CharField | Classification type |
| description | TextField | Optional description |
| created_at | DateTimeField | Timestamp when classification was created |
| updated_at | DateTimeField | Timestamp when classification was last updated |

### HoldingClass

Mapping between holdings and classifications.

| Field | Type | Description |
|-------|------|-------------|
| id | BigAutoField | Primary key |
| holding | ForeignKey | Associated holding |
| classification | ForeignKey | Associated classification |
| created_at | DateTimeField | Timestamp when mapping was created |
| updated_at | DateTimeField | Timestamp when mapping was last updated |
