# Superadmin Control Panel

## Overview
The Superadmin Control Panel is a comprehensive dashboard for managing all aspects of the booking system.

## Features

### 1. Dashboard Analytics
- Total users, services, bookings, and revenue statistics
- User breakdown (Providers, Customers, Superadmins)
- Booking statistics (Pending, Completed)
- Recent users and bookings
- Top services by booking count

### 2. User Management
- View all users with search functionality
- Filter by user type (All, Customers, Providers, Superadmins)
- View user details: username, name, email, join date, last login
- User statistics dashboard

### 3. Service Management
- View all services across the platform
- Filter by status (Active/Inactive)
- Search by service name or provider
- Service statistics and details

### 4. Bulk Notification System
- Send notifications to all users, customers only, or providers only
- Multiple notification types: System, Booking, Message, Reminder
- View recent notification history
- Bulk messaging capability

## Access Information

### Creating a Superadmin User

Run the following command to create a superadmin user:

```bash
python manage.py create_superadmin
```

This will create a superadmin account with the following credentials:

- **Username**: `superadmin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

**Important**: Please change the password after first login!

### Logging In

1. Go to the login page: `http://localhost:8000/login/`
2. Enter the superadmin credentials (username: `superadmin`, password: `admin123`)
3. Select either "User" or "Provider" (superadmin can login with either)
4. You will be automatically redirected to the Superadmin Control Panel

### Accessing the Panel

Once logged in as superadmin, you can access the panel at:
- Direct URL: `http://localhost:8000/superadmin/`
- Or click "Superadmin Panel" in the sidebar navigation

## Navigation

The Superadmin Control Panel has four main sections:

1. **Dashboard** (`/superadmin/`) - Analytics and overview
2. **Users** (`/superadmin/users/`) - User management interface
3. **Services** (`/superadmin/services/`) - Service management interface
4. **Notifications** (`/superadmin/notifications/`) - Bulk notification system

## Security

- Only users with `user_type='superadmin'` can access the panel
- All views are protected with the `@superadmin_required` decorator
- Unauthorized access attempts redirect to the regular dashboard with an error message

## Design

- High-end Bootstrap 5 design with purple-to-violet gradient theme
- Glassmorphism effects on headers
- Smooth hover animations and transitions
- Responsive layout for all screen sizes
- Professional typography with Inter font
- Color-coded badges for different statuses
