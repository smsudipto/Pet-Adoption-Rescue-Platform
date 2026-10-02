from django.contrib import admin
from .models import AdoptionRequest

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'pet__name', 'phone')
    
    def save_model(self, request, obj, form, change):
        if change:
            original = AdoptionRequest.objects.get(pk=obj.pk)
            # Rule 3: When admin approves an application, Pet Status = Adopted[cite: 1]
            if original.status != 'Approved' and obj.status == 'Approved':
                pet = obj.pet
                pet.status = 'Adopted'
                pet.save()
        super().save_model(request, obj, form, change)