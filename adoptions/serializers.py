from rest_framework import serializers
from .models import AdoptionRequest

class AdoptionRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    pet_name = serializers.CharField(source='pet.name', read_only=True)

    class Meta:
        model = AdoptionRequest
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at']