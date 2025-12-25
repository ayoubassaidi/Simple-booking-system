# Login & Dashboard System - Complete Guide

## Overview

This Django project now includes a professional **Login & Dashboard System** with elegant UI/UX design using Bootstrap 5, Google Fonts, and modern web design principles.

---

## Features

### Login Page
- **Glassmorphism Design**: Clean, modern card with subtle backdrop blur
- **Professional Icons**: Bootstrap Icons for visual appeal
- **Google Fonts**: Uses 'Poppins' for elegant typography
- **Form Validation**: Built-in Django authentication with error messages
- **Responsive Design**: Works perfectly on all devices

### Dashboard
- **Sidebar Navigation**: Fixed sidebar with menu items
  - Dashboard (Home)
  - Profile
  - Bookings
  - Notifications
  - Settings
  - Logout
- **Quick Stats Cards**: 4 beautiful cards showing:
  - Account Status
  - Member Since
  - Last Login
  - Notifications Count
- **Account Information Section**: Detailed user info display
- **Modern Grid Layout**: Bootstrap 5 grid system
- **Google Fonts**: Uses 'Inter' for clean, professional look

---

## File Structure

```
accounts/
├── views.py                    # Login & dashboard logic
├── urls.py                     # URL routing
└── templates/accounts/
    ├── login.html             # Login page
    └── dashboard.html         # User dashboard
```

---

## URL Routes

| URL | View | Description | Login Required |
|-----|------|-------------|----------------|
| `/login/` | LoginView | User login page | No |
| `/logout/` | LogoutView | Logout and redirect to login | No |
| `/dashboard/` | dashboard | User dashboard | Yes |

---

## Code Explanation (For Beginners)

### 1. views.py

```python
@login_required
def dashboard(request):
    """User dashboard - only accessible when logged in"""
    # The @login_required decorator protects this view
    # If user is not logged in, they're redirected to login page

    # Get user's profile to display user type
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_type = user_profile.get_user_type_display()
    except UserProfile.DoesNotExist:
        user_type = "User"

    # Prepare data to send to the template
    context = {
        'username': request.user.username,
        'user_type': user_type,
        'email': request.user.email if request.user.email else 'Not provided',
        'date_joined': request.user.date_joined,
        'last_login': request.user.last_login,
    }

    return render(request, 'accounts/dashboard.html', context)
```

**What this does:**
1. `@login_required` ensures only logged-in users can access the dashboard
2. Retrieves the user's profile information from the database
3. Prepares data (username, email, join date, etc.) to display
4. Sends all data to the template for rendering

### 2. urls.py

```python
urlpatterns = [
    # Login using Django's built-in LoginView
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),

    # Logout using Django's built-in LogoutView
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Dashboard (protected by @login_required)
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

**What this does:**
1. Uses Django's **built-in LoginView** - no need to write login logic!
2. Uses Django's **built-in LogoutView** - automatic logout handling
3. Routes `/dashboard/` to our custom dashboard view

### 3. settings.py

```python
# Login & Logout Redirects
LOGIN_URL = 'login'                  # Where to redirect if not logged in
LOGIN_REDIRECT_URL = 'dashboard'     # Where to go after successful login
LOGOUT_REDIRECT_URL = 'login'        # Where to go after logout
```

**What this does:**
- Tells Django where to redirect users in different scenarios
- Makes the login flow automatic and seamless

---

## How to Use the System

### Step 1: Start the Server

```bash
cd "/Users/ayoubassaidi/Desktop/FInal project - Booking/booking_project/booking_project"
source venv/bin/activate
python manage.py runserver
```

### Step 2: Access the Login Page

Open your browser and go to:
```
http://127.0.0.1:8000/login/
```

### Step 3: Test Login

**Option A: Create a new user through registration**
1. Go to `http://127.0.0.1:8000/`
2. Click "Register as User" or "Register as Service Provider"
3. Fill in the registration form
4. You'll be automatically logged in and redirected to the dashboard

**Option B: Use the admin account (already created)**
- Username: `admin`
- Password: You'll need to set this manually

To set admin password:
```bash
python manage.py changepassword admin
```

### Step 4: Explore the Dashboard

Once logged in, you'll see:
- Welcome message with your username
- Quick stats cards
- Sidebar navigation
- Account information section

### Step 5: Logout

Click the "Logout" button in:
- The sidebar menu, OR
- The header section

You'll be redirected back to the login page.

---

## Design Details

### Color Scheme
- **Primary Gradient**: `#667eea` to `#764ba2` (Purple gradient)
- **Background**: `#f8f9fa` (Light gray)
- **Cards**: White with subtle shadows
- **Text**: Dark gray `#333` for headings, `#6c757d` for body

### Typography
- **Login Page**: Poppins (Google Font)
- **Dashboard**: Inter (Google Font)
- **Icon Library**: Bootstrap Icons 1.10.0

### Responsive Design
- Desktop: Full sidebar + content layout
- Mobile: Sidebar collapses (can be expanded with hamburger menu)

---

## Customization Guide

### Change the Gradient Colors

In `login.html` and `dashboard.html`, find:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Replace `#667eea` and `#764ba2` with your preferred colors.

### Add More Sidebar Menu Items

In `dashboard.html`, add to the sidebar menu:
```html
<li>
    <a href="{% url 'your_url_name' %}">
        <i class="bi bi-your-icon"></i>
        <span>Your Menu Item</span>
    </a>
</li>
```

### Customize Quick Stats

In `views.py`, add more data to the context:
```python
context = {
    'username': request.user.username,
    'your_custom_stat': 'Your Value',
}
```

Then display it in the template.

---

## Security Features

1. **@login_required Decorator**: Protects dashboard from unauthorized access
2. **CSRF Protection**: All forms include `{% csrf_token %}`
3. **Django's Built-in Auth**: Uses secure, tested authentication system
4. **Session Management**: Automatic session handling by Django

---

## Troubleshooting

### Problem: "Page not found" when accessing `/dashboard/`

**Solution**: Make sure you're logged in first. Go to `/login/`

### Problem: Login form doesn't work

**Solution**:
1. Make sure the server is running
2. Check that you're using the correct username/password
3. Verify that the user exists in the database

### Problem: Can't see the user type on dashboard

**Solution**:
- If you registered through the registration form, the UserProfile is created automatically
- If you created a user through admin or `createsuperuser`, you need to manually create a UserProfile:
  ```bash
  python manage.py shell
  ```
  ```python
  from django.contrib.auth.models import User
  from accounts.models import UserProfile
  user = User.objects.get(username='admin')
  UserProfile.objects.create(user=user, user_type='user')
  ```

---

## Next Steps

You can extend this system by:

1. **Add Password Reset**: Use Django's `PasswordResetView`
2. **Add Profile Editing**: Create a form to edit user information
3. **Add Real Booking Functionality**: Create booking models and views
4. **Add Email Verification**: Require email confirmation on registration
5. **Add User Avatar**: Allow users to upload profile pictures

---

## Summary

This login and dashboard system provides:
- Professional, modern UI/UX
- Simple, beginner-friendly code
- Secure authentication using Django's built-in views
- Responsive design that works on all devices
- Easy customization and extension

All files are ready to use - just run the server and start exploring!
