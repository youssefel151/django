from django.conf import settings
from django.db import models


class ProfilUtilisateur(models.Model):
    ADMIN = 'admin'
    ENSEIGNANT = 'enseignant'
    ETUDIANT = 'etudiant'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (ENSEIGNANT, 'Enseignant'),
        (ETUDIANT, 'Etudiant'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profil')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ETUDIANT)

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

class Record(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    zipcode=models.CharField(max_length=20)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")
