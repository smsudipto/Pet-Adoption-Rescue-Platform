from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdoptionRequestViewSet, apply_adoption_view, user_dashboard_view

router = DefaultRouter()
router.register(r'api/adoptions', AdoptionRequestViewSet, basename='adoption-api')

urlpatterns = [
    path('adopt/<int:pet_id>/', apply_adoption_view, name='apply_adoption'),
    path('dashboard/', user_dashboard_view, name='user_dashboard'),
    path('', include(router.urls)),
]