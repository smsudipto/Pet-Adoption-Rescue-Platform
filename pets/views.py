from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pet, Favorite
from .serializers import PetSerializer

# --- DRF API ViewSet ---
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all().order_by('-created_at')
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['animal_type', 'gender', 'location', 'status', 'breed']
    search_fields = ['name', 'breed', 'location', 'description']


# --- Django Template Views ---
def home_view(request):
    featured_pets = Pet.objects.filter(status='Available').order_by('-created_at')[:6]
    return render(request, 'home.html', {'featured_pets': featured_pets})

def pet_list_view(request):
    pets = Pet.objects.all().order_by('-created_at')
    
    # Simple search & filter logic for templates
    query = request.GET.get('search')
    animal_type = request.GET.get('animal_type')
    gender = request.GET.get('gender')
    location = request.GET.get('location')
    status = request.GET.get('status')
    breed = request.GET.get('breed')
    
    if query:
        pets = pets.filter(name__icontains=query) | pets.filter(breed__icontains=query)
    if animal_type:
        pets = pets.filter(animal_type=animal_type)
    if gender:
        pets = pets.filter(gender=gender)
    if location:
        pets = pets.filter(location__icontains=location)
    if status:
        pets = pets.filter(status=status)
    if breed:
        pets = pets.filter(breed__icontains=breed)
        
    # Web Pagination (Prottek page-e 6 ta pet thakbe)
    paginator = Paginator(pets, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
        'pets': page_obj,
    }
    return render(request, 'pet_list.html', context)

def pet_detail_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, 'pet_detail.html', {'pet': pet})


# --- Favorite System Views ---
@login_required
def toggle_favorite(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, pet=pet)
    if not created:
        favorite.delete()  # Age theke thakle remove hoye jabe
    return redirect('pet_detail', pk=pet_id)

@login_required
def favorite_list_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('pet')
    return render(request, 'favorite_list.html', {'favorites': favorites})