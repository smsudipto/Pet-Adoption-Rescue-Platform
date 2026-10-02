from django.urls import path
from .views import (
    register_view, 
    login_view, 
    logout_view, 
    UserRegistrationView, 
    UserProfileView
)

urlpatterns = [
    # Template-based Web URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # REST API Endpoints
    path('api/register/', UserRegistrationView.as_view(), name='api_register'),
    path('api/profile/', UserProfileView.as_view(), name='api_profile'),
]