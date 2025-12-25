# Smart Service Booking - Django Full Authentication System

A complete, professional authentication system built with Django and Bootstrap 5, featuring:
- User Registration (User vs Service Provider)
- Professional Login & Logout
- Protected User Dashboard with modern UI/UX

## Project Structure

```
booking_project/
├── manage.py
├── venv/                          # Virtual environment
├── booking_system/                # Main project folder
│   ├── settings.py               # Project settings
│   └── urls.py                   # Main URL configuration
└── accounts/                      # Registration app
    ├── models.py                 # UserProfile model
    ├── views.py                  # Registration views
    ├── urls.py                   # App URL configuration
    └── templates/accounts/
        ├── base.html            # Base template with Bootstrap
        ├── index.html           # Landing page (account choice)
        ├── register.html        # Registration form
        ├── success.html         # Success page
        ├── login.html           # Login page (NEW!)
        └── dashboard.html       # User dashboard (NEW!)
```

## Features

### Registration System
- Modern, responsive landing page with two registration options
- User type selection (User vs Service Provider)
- Clean registration forms using Django's UserCreationForm
- Success page with user information
- Bootstrap 5 styling with gradient design

### Login & Dashboard System (NEW!)
- Professional login page with glassmorphism design
- Protected user dashboard with sidebar navigation
- Quick stats cards (Account Status, Member Since, Last Login, Notifications)
- Modern grid layout using Bootstrap 5
- Google Fonts (Poppins for login, Inter for dashboard)
- Fully beginner-friendly code using Django's built-in auth views

## How to Run the Project

1. **Navigate to the project directory:**
   ```bash
   cd "/Users/ayoubassaidi/Desktop/FInal project - Booking/booking_project/booking_project"
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

4. **Open your browser and visit:**
   ```
   http://127.0.0.1:8000/
   ```

## Pages and URLs

- **Home/Landing Page**: `http://127.0.0.1:8000/`
  - Shows two cards for account type selection

- **User Registration**: `http://127.0.0.1:8000/register/user/`
  - Registration form for regular users

- **Provider Registration**: `http://127.0.0.1:8000/register/provider/`
  - Registration form for service providers

- **Login Page**: `http://127.0.0.1:8000/login/` (NEW!)
  - Professional login form with modern design

- **Dashboard**: `http://127.0.0.1:8000/dashboard/` (NEW!)
  - Protected user dashboard (requires login)

- **Logout**: `http://127.0.0.1:8000/logout/` (NEW!)
  - Logs out user and redirects to login

- **Success Page**: `http://127.0.0.1:8000/success/`
  - Shown after successful registration

- **Admin Panel**: `http://127.0.0.1:8000/admin/`
  - Django admin interface

## Code Explanation (For Beginners)

### models.py
```python
# Creates a UserProfile that extends Django's default User model
# Stores the user type (user or provider)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
```

### views.py
- `index()` - Shows the landing page with account type choices
- `register_user()` - Handles user registration form
- `register_provider()` - Handles provider registration form
- `success()` - Shows success message after registration
- `dashboard()` - Protected dashboard view (requires @login_required decorator)

### urls.py
- Uses Django's built-in `LoginView` and `LogoutView` for authentication
- Simple, beginner-friendly URL routing

### Templates
- `base.html` - Contains Bootstrap CSS/JS and header
- `index.html` - Landing page with two cards
- `register.html` - Reusable registration form
- `success.html` - Success confirmation page
- `login.html` - Professional login page with glassmorphism design
- `dashboard.html` - Modern dashboard with sidebar and stats cards

## Quick Start Guide

### Test the Login System

A test admin account has been created for you:
- **Username**: `admin`
- **Password**: (not set yet)

To set the password:
```bash
python manage.py changepassword admin
```

Then visit `http://127.0.0.1:8000/login/` and log in!

### Create a New User

**Option 1: Through Registration Form**
1. Go to `http://127.0.0.1:8000/`
2. Click "Register as User" or "Register as Service Provider"
3. Fill out the form and submit
4. You'll be automatically logged in and redirected to the dashboard!

**Option 2: Through Admin Panel**
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account, then visit `http://127.0.0.1:8000/admin/`

## Documentation

For detailed information about the Login & Dashboard system, see:
- [LOGIN_GUIDE.md](LOGIN_GUIDE.md) - Complete guide with code explanations

## Next Steps

You can extend this project by:
1. Adding email verification
2. Adding profile editing functionality
3. Creating provider-specific dashboard features
4. Implementing actual booking functionality
5. Adding service listings for providers
6. Adding password reset functionality
7. Adding user avatars/profile pictures

## Technologies Used

- Django 4.2.27
- Bootstrap 5.3.0
- Bootstrap Icons 1.10.0
- SQLite (default Django database)

## File Locations for VS Code

All files are located in:
```
/Users/ayoubassaidi/Desktop/FInal project - Booking/booking_project/booking_project/
```

You can open this folder directly in VS Code to edit the files!
