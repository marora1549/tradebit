# TradeBit Frontend Architecture

This document describes the architecture and design decisions for the TradeBit frontend.

## Technology Stack

- **React**: Library for building user interfaces
- **TypeScript**: Typed superset of JavaScript
- **React Router**: Routing library for React
- **React Query**: Data fetching and state management
- **React Hook Form**: Form validation and handling
- **Zustand**: Lightweight state management
- **Axios**: HTTP client
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: UI component library based on Tailwind CSS
- **Recharts**: Charting library for React

## Project Structure

```
src/
├── components/        # Reusable components
│   ├── ui/            # Base UI components
│   ├── Dashboard/     # Dashboard-specific components
│   ├── Portfolio/     # Portfolio-specific components
│   ├── Settings/      # Settings-specific components
│   └── ...            # Other component categories
├── layouts/           # Page layouts
│   ├── AuthLayout.tsx # Layout for authentication pages
│   └── DashboardLayout.tsx # Layout for dashboard pages
├── pages/             # Page components
│   ├── auth/          # Authentication pages
│   ├── Dashboard.tsx  # Dashboard page
│   ├── Portfolio.tsx  # Portfolio page
│   ├── Settings.tsx   # Settings page
│   └── ...            # Other pages
├── services/          # API services
│   ├── api.ts         # API client configuration
│   ├── auth.ts        # Authentication service
│   └── ...            # Other services
├── stores/            # State stores
│   ├── authStore.ts   # Authentication state
│   └── ...            # Other stores
├── utils/             # Utility functions
├── App.tsx            # Main application component
└── index.tsx          # Entry point
```

## State Management

TradeBit uses a combination of state management approaches:

- **Local Component State**: For UI-specific state
- **React Query**: For server state (data fetching, caching, updates)
- **Zustand**: For global application state (auth, user preferences, etc.)

### Authentication State

The authentication state is managed using Zustand. The `authStore` handles:

- User authentication status
- User information
- Login/logout actions
- Token management and refresh

## Routing

Routing is handled by React Router with the following main routes:

- `/auth/*`: Authentication routes
  - `/auth/login`: Login page
  - `/auth/register`: Registration page
- `/`: Dashboard page (default route)
- `/portfolio`: Portfolio page
- `/zerodha`: Zerodha integration page
- `/settings`: Settings page

Protected routes are implemented using a `ProtectedRoute` component that redirects unauthenticated users to the login page.

## Styling

TradeBit uses Tailwind CSS for styling with the following customizations:

- Custom color scheme with primary colors
- Dark mode support
- Responsive design for mobile, tablet, and desktop

The UI components are based on shadcn/ui, which provides a set of accessible and customizable components built on top of Tailwind CSS.

## Data Fetching

Data fetching is done using React Query, which provides:

- Automatic caching and deduplication
- Background refetching
- Optimistic updates
- Error handling
- Loading states

The API client is configured using Axios with JWT token authentication and automatic token refresh.

## Forms

Forms are implemented using React Hook Form, which provides:

- Form validation
- Error handling
- Field management
- Form submission

## Charts and Visualizations

Charts are implemented using Recharts, a composable charting library for React. The main charts include:

- Portfolio value over time
- Sector allocation
- Holdings distribution

## Component Design

### Base UI Components

Base UI components are reusable components that form the building blocks of the UI:

- `Button`: Customizable button component
- `Card`: Card container with header, content, and footer
- `Input`: Text input component
- And more...

### Dashboard Components

- `PortfolioSummary`: Displays a summary of the user's portfolio
- `RecentActivity`: Shows recent portfolio activity
- `MarketOverview`: Provides an overview of the market

### Portfolio Components

- `HoldingsList`: Displays a list of the user's holdings
- `HoldingDetails`: Shows detailed information about a holding
- `AddHoldingForm`: Form for adding a new holding

### Settings Components

- `UserProfileForm`: Form for updating user profile
- `ZerodhaSettingsForm`: Form for configuring Zerodha API credentials
- `PreferencesForm`: Form for updating user preferences

## Best Practices

- **Code Splitting**: Pages and large components are loaded lazily
- **Accessibility**: UI components follow WAI-ARIA guidelines
- **Error Boundaries**: Catch and handle runtime errors
- **Performance Optimization**: Memoization, virtualization for large lists
- **Type Safety**: TypeScript for static type checking
- **Testing**: Unit tests for components and utilities
