from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    ANIMAL_TYPES = (
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Bird', 'Bird'),
        ('Rabbit', 'Rabbit'),
        ('Other', 'Other'),
    )
    
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Adopted', 'Adopted'),
    )

    name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=50, choices=ANIMAL_TYPES)
    breed = models.CharField(max_length=100)
    age = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='pet_images/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.animal_type})"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pet')

    def __str__(self):
        return f"{self.user.username} - {self.pet.name}"