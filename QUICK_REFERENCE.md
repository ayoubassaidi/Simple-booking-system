# Quick Reference - Django Authentication System

## File Locations

```
booking_project/booking_project/
├── accounts/
│   ├── views.py                           # All view functions
│   ├── urls.py                            # URL routing
│   ├── models.py                          # UserProfile model
│   └── templates/accounts/
│       ├── login.html                    # Login page
│       ├── dashboard.html                # Dashboard page
│       ├── index.html                    # Home/landing page
│       ├── register.html                 # Registration form
│       └── success.html                  # Success page
├── booking_system/
│   ├── settings.py                       # Project settings
│   └── urls.py                           # Main URL config
└── manage.py                              # Django management script
```

---

## Key Code Snippets

### 1. Protected View (views.py)
```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Only logged-in users can access this
    context = {
        'username': request.user.username,
        'email': request.user.email,
    }
    return render(request, 'accounts/dashboard.html', context)
```

### 2. URL Routing (urls.py)
```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Built-in Login View
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),

    # Built-in Logout View
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Custom Dashboard View
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

### 3. Login Redirects (settings.py)
```python
LOGIN_URL = 'login'                  # Where to go if not logged in
LOGIN_REDIRECT_URL = 'dashboard'     # Where to go after login
LOGOUT_REDIRECT_URL = 'login'        # Where to go after logout
```

### 4. Template - Accessing User Data
```html
<!-- In dashboard.html -->
<h2>Welcome, {{ username }}!</h2>
<p>Email: {{ email }}</p>
<p>Joined: {{ date_joined|date:"F d, Y" }}</p>
```

### 5. Template - Logout Link
```html
<a href="{% url 'logout' %}">Logout</a>
```

---

## Common Tasks

### Run the Server
```bash
cd "/Users/ayoubassaidi/Desktop/FInal project - Booking/booking_project/booking_project"
source venv/bin/activate
python manage.py runserver
```

### Create a User
```bash
python manage.py createsuperuser
```

### Change User Password
```bash
python manage.py changepassword username
```

### Make Migrations (after model changes)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Access Django Shell
```bash
python manage.py shell
```

---

## URL Cheat Sheet

| Page | URL | Login Required? |
|------|-----|-----------------|
| Home | `http://127.0.0.1:8000/` | No |
| Login | `http://127.0.0.1:8000/login/` | No |
| Dashboard | `http://127.0.0.1:8000/dashboard/` | Yes |
| Logout | `http://127.0.0.1:8000/logout/` | No |
| Register (User) | `http://127.0.0.1:8000/register/user/` | No |
| Register (Provider) | `http://127.0.0.1:8000/register/provider/` | No |
| Admin | `http://127.0.0.1:8000/admin/` | Yes |

---

## Django Template Tags

### Check if User is Logged In
```html
{% if user.is_authenticated %}
    <p>Hello, {{ user.username }}!</p>
{% else %}
    <a href="{% url 'login' %}">Please login</a>
{% endif %}
```

### URL Reverse Lookup
```html
<a href="{% url 'dashboard' %}">Go to Dashboard</a>
<a href="{% url 'login' %}">Login</a>
<a href="{% url 'logout' %}">Logout</a>
```

### CSRF Token (Required in Forms)
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields here -->
    <button type="submit">Submit</button>
</form>
```

### Date Formatting
```html
{{ date_joined|date:"F d, Y" }}           <!-- December 25, 2025 -->
{{ last_login|date:"M d, Y - g:i A" }}    <!-- Dec 25, 2025 - 2:30 PM -->
```

---

## User Object Properties

Access these in templates with `{{ user.property }}` or in views with `request.user.property`:

- `user.username` - Username
- `user.email` - Email address
- `user.first_name` - First name
- `user.last_name` - Last name
- `user.is_authenticated` - True if logged in
- `user.is_staff` - True if staff member
- `user.is_superuser` - True if admin
- `user.date_joined` - When account was created
- `user.last_login` - Last login datetime

---

## Customization Tips

### Change Colors
Look for these in the template files:
```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your colors */
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Add New Sidebar Menu Item
In `dashboard.html`, add:
```html
<li>
    <a href="{% url 'your_view_name' %}">
        <i class="bi bi-icon-name"></i>
        <span>Menu Item</span>
    </a>
</li>
```

### Add New Stat Card
In `dashboard.html`, copy and paste a stat card:
```html
<div class="stat-card primary">
    <div class="stat-icon">
        <i class="bi bi-your-icon"></i>
    </div>
    <h6>Your Label</h6>
    <p class="stat-value">{{ your_value }}</p>
</div>
```

---

## Troubleshooting

### Error: "Page not found at /dashboard/"
**Fix**: Make sure you're logged in. Visit `/login/` first.

### Error: "CSRF verification failed"
**Fix**: Make sure `{% csrf_token %}` is in your form.

### Error: "TemplateDoesNotExist"
**Fix**: Check that the template file exists in `accounts/templates/accounts/`

### Can't login
**Fix**:
1. Check username/password are correct
2. Make sure the user exists: `python manage.py createsuperuser`
3. Reset password: `python manage.py changepassword username`

---

## Bootstrap Icons Reference

Used in the project:
- `bi-person-circle` - User icon
- `bi-briefcase-fill` - Provider icon
- `bi-shield-lock-fill` - Lock/security
- `bi-speedometer2` - Dashboard
- `bi-calendar-check` - Bookings
- `bi-bell` - Notifications
- `bi-gear` - Settings
- `bi-box-arrow-right` - Logout

Find more at: https://icons.getbootstrap.com/

---

## Resources

- **Django Docs**: https://docs.djangoproject.com/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.3/
- **Bootstrap Icons**: https://icons.getbootstrap.com/
- **Google Fonts**: https://fonts.google.com/

---

## Project Status

✅ Registration System (Complete)
✅ Login/Logout System (Complete)
✅ Protected Dashboard (Complete)
⏳ Profile Editing (To Do)
⏳ Booking System (To Do)
⏳ Email Verification (To Do)
