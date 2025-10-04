from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'tracker'

urlpatterns = [
    # Homepage - landing page atau dashboard
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='tracker:home'), name='logout'),
    
    # Dashboard - halaman utama tracker (login required)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # User Profile
    path('profile/', views.profile_view, name='profile'),
    
    # CRUD Activities (login required)
    path('add-activity/', views.add_activity, name='add_activity'),
    path('edit-activity/<int:activity_id>/', views.edit_activity, name='edit_activity'),
    path('delete-activity/<int:activity_id>/', views.delete_activity, name='delete_activity'),
    
    # AJAX endpoints (login required)
    path('toggle-activity/', views.toggle_activity, name='toggle_activity'),
    
    # Statistics (login required)
    path('stats/', views.stats, name='stats'),
]