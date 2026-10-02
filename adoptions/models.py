from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet

class AdoptionRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    reason = models.TextField()
    previous_pet_experience = models.CharField(max_length=10, choices=(('Yes', 'Yes'), ('No', 'No')))
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pet.name} ({self.status})"