from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-started/', views.index, name='index'),
    path('register/user/', views.register_user, name='register_user'),
    path('register/provider/', views.register_provider, name='register_provider'),
    path('success/', views.success, name='success'),

    # Login & Logout using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Dashboard (protected by login_required)
    path('dashboard/', views.dashboard, name='dashboard'),
]
