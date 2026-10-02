from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PetViewSet, 
    home_view, 
    pet_list_view, 
    pet_detail_view, 
    toggle_favorite, 
    favorite_list_view
)

# DRF Router setup
router = DefaultRouter()
router.register(r'pets-api', PetViewSet, basename='pet-api')

urlpatterns = [
    path('', home_view, name='home'),
    path('pets/', pet_list_view, name='pet_list'),
    path('pets/<int:pk>/', pet_detail_view, name='pet_detail'),
    
    # Favorite Feature URLs Added Here
    path('favorites/', favorite_list_view, name='favorite_list'),
    path('pet/<int:pet_id>/favorite/', toggle_favorite, name='toggle_favorite'),
    
    path('api/', include(router.urls)),
]