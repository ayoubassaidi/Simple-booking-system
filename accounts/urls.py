from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-started/', views.index, name='index'),
    path('register/user/', views.register_user, name='register_user'),
    path('register/provider/', views.register_provider, name='register_provider'),
    path('success/', views.success, name='success'),

    # Login & Logout
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Dashboard (protected by login_required)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Profile & Notifications
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),

    # Superadmin Routes
    path('superadmin/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin/users/', views.superadmin_users, name='superadmin_users'),
    path('superadmin/services/', views.superadmin_services, name='superadmin_services'),
    path('superadmin/notifications/', views.superadmin_notifications, name='superadmin_notifications'),
]
