# Project Structure Documentation

This document describes the reorganized structure of the Simple Booking System Django project.

## Overview

The project has been restructured to use **global static files** and **global templates**, following Django best practices. This makes the codebase more maintainable, reduces duplication, and provides a consistent look and feel across the application.

## Directory Structure

```
Simple-booking-system/
├── static/                          # Global static files
│   ├── css/
│   │   ├── base.css                # Styles for public pages (login, register, index)
│   │   └── dashboard.css           # Styles for dashboard/authenticated pages
│   ├── js/
│   │   └── main.js                 # Global JavaScript functionality
│   └── images/                     # Global images (logo, icons, etc.)
│
├── templates/                       # Global templates
│   ├── base.html                   # Base template for public pages
│   ├── dashboard_base.html         # Base template for dashboard pages
│   └── login.html                  # Login page template
│
├── accounts/                        # Accounts app
│   └── templates/accounts/         # App-specific templates
│       ├── index.html              # Landing/home page
│       ├── register.html           # Registration form
│       ├── dashboard.html          # User dashboard
│       └── success.html            # Success page
│
├── bookings/                        # Bookings app
│   └── templates/bookings/         # App-specific templates
│       └── add_availability.html   # Add availability form
│
└── booking_system/                  # Project settings
    └── settings.py                 # Django settings (configured for global static/templates)
```

## Static Files Organization

### CSS Files

1. **base.css** - Public pages styling
   - Login page
   - Registration pages
   - Landing page
   - Includes: gradient backgrounds, card styles, form styles, button styles

2. **dashboard.css** - Dashboard styling
   - Sidebar navigation
   - Dashboard header
   - Stats cards
   - Main content sections
   - Tables and data displays
   - Responsive design for mobile

### JavaScript Files

1. **main.js** - Global JavaScript functionality
   - Mobile menu toggle
   - Active menu item highlighting
   - Form validation helpers
   - Toast notifications
   - Date picker enhancements
   - Auto-dismiss alerts

## Templates Organization

### Global Templates

1. **base.html** - Base template for public pages
   - Used by: index, register, login
   - Includes: Bootstrap, Bootstrap Icons, Google Fonts, global CSS
   - Blocks: `title`, `extra_css`, `header_subtitle`, `content`, `extra_js`

2. **dashboard_base.html** - Base template for authenticated pages
   - Used by: dashboard, add_availability
   - Includes: Sidebar navigation, dashboard header, user info
   - Blocks: `title`, `extra_css`, `page_title`, `page_subtitle`, `header_actions`, `dashboard_content`, `extra_js`

3. **login.html** - Standalone login page
   - Extends base.html
   - Custom styled login form with account type selector

### App-Specific Templates

Templates in app directories extend the global base templates:

- **accounts/index.html** - Extends `base.html`
- **accounts/register.html** - Extends `base.html`
- **accounts/dashboard.html** - Extends `dashboard_base.html`
- **bookings/add_availability.html** - Extends `dashboard_base.html`

## How to Use

### Creating a New Public Page

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}My Page Title{% endblock %}

{% block extra_css %}
<style>
    /* Page-specific styles */
</style>
{% endblock %}

{% block content %}
    <!-- Your page content here -->
{% endblock %}
```

### Creating a New Dashboard Page

```html
{% extends 'dashboard_base.html' %}

{% block title %}Dashboard Page{% endblock %}

{% block page_title %}Welcome to My Page{% endblock %}

{% block page_subtitle %}Subtitle text here{% endblock %}

{% block dashboard_content %}
    <!-- Your dashboard content here -->
{% endblock %}
```

### Adding Custom CSS

For page-specific styles, use the `extra_css` block:

```html
{% block extra_css %}
<style>
    .custom-class {
        /* Your custom styles */
    }
</style>
{% endblock %}
```

### Adding Custom JavaScript

For page-specific JavaScript, use the `extra_js` block:

```html
{% block extra_js %}
<script>
    // Your custom JavaScript
</script>
{% endblock %}
```

## Configuration

### settings.py

The following settings enable global static files and templates:

```python
# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates directory
        'APP_DIRS': True,
        # ... other settings
    },
]

# Static files configuration
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Global static files directory
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

## Benefits of This Structure

1. **No Code Duplication** - CSS and JS are in one place
2. **Consistent Design** - All pages use the same base styles
3. **Easy Maintenance** - Update styles globally from one location
4. **Better Organization** - Clear separation between global and app-specific files
5. **Scalability** - Easy to add new apps and pages
6. **Django Best Practices** - Follows Django's recommended project structure

## Development Workflow

### Collecting Static Files for Production

Before deploying to production, run:

```bash
python manage.py collectstatic
```

This collects all static files into the `staticfiles` directory.

### Adding New Static Files

1. Add CSS files to `static/css/`
2. Add JS files to `static/js/`
3. Add images to `static/images/`
4. Reference in templates using `{% static 'path/to/file' %}`

### Creating New Pages

1. Create template in appropriate location:
   - Public pages → Extend `base.html`
   - Dashboard pages → Extend `dashboard_base.html`
2. Add view in the appropriate app's `views.py`
3. Add URL pattern in the app's `urls.py`

## Notes

- Always use `{% load static %}` at the top of templates that use static files
- The `static/images/` directory is ready for logos, icons, and other images
- Mobile responsiveness is built into the CSS
- Bootstrap 5 and Bootstrap Icons are loaded via CDN
- Google Fonts (Inter) is used for dashboard pages

## Next Steps

Consider adding:
- Custom 404/500 error pages in the global templates directory
- Additional CSS files for specific features (e.g., `forms.css`, `tables.css`)
- JavaScript modules for complex functionality
- Image assets (logo, favicon, etc.)
