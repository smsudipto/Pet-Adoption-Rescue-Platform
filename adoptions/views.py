from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError

from pets.models import Pet
from .models import AdoptionRequest
from .serializers import AdoptionRequestSerializer

# --- Template Views (Django Web Interface) ---

@login_required
def apply_adoption_view(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    
    # Business Logic Rule 1: Only available pets can be adopted[cite: 1]
    if pet.status != 'Available':
        messages.error(request, "This pet has already been adopted and is no longer available.")
        return redirect('pet_detail', pk=pet.id)
    
    # Business Logic Rule 2: One user cannot submit multiple active requests for the same pet[cite: 1]
    existing_request = AdoptionRequest.objects.filter(user=request.user, pet=pet, status='Pending').exists()
    if existing_request:
        messages.warning(request, "You already have a pending adoption request for this pet.")
        return redirect('user_dashboard')
        
    if request.method == 'POST':
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        reason = request.POST.get('reason')
        previous_pet_experience = request.POST.get('previous_pet_experience')
        message = request.POST.get('message')
        
        AdoptionRequest.objects.create(
            user=request.user,
            pet=pet,
            phone=phone,
            address=address,
            reason=reason,
            previous_pet_experience=previous_pet_experience,
            message=message
        )
        messages.success(request, "Adoption application submitted successfully!")
        return redirect('user_dashboard')
        
    return render(request, 'adoption_form.html', {'pet': pet})

@login_required
def user_dashboard_view(request):
    user_requests = AdoptionRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_dashboard.html', {'user_requests': user_requests})


# --- REST API ViewSets (Django REST Framework) ---

class AdoptionRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AdoptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users should only be able to access their own adoption requests[cite: 1]
        return AdoptionRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        pet = serializer.validated_data['pet']
        
        # Rule 1: Only available pets can be adopted[cite: 1]
        if pet.status != 'Available':
            raise ValidationError("This pet has already been adopted.")
            
        # Rule 2: One user cannot submit multiple active requests for the same pet[cite: 1]
        existing = AdoptionRequest.objects.filter(user=self.request.user, pet=pet, status='Pending').exists()
        if existing:
            raise ValidationError("You already have a pending request for this pet.")
            
        serializer.save(user=self.request.user)