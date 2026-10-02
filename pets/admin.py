from django.contrib import admin
from .models import Pet

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'breed', 'location', 'status')
    list_filter = ('animal_type', 'status', 'gender', 'location')
    search_fields = ('name', 'breed', 'location')