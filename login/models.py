from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import RegexValidator
from django.db import models


phone_number_validator = RegexValidator(
    regex=r'^\d{10}$', 
    message="Enter a valid 10-digit phone number."
)

class UserDetails(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE) 
    date_of_birth = models.DateField(default=None)
    user_status = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=10, validators=[phone_number_validator],unique=True)

    def __str__(self): 
        return self.user_profile.username



class LicenseDetails(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE) 
    license_number = models.CharField(max_length=50,unique=True)
    district_name = models.CharField(max_length=50)
    licensee_name = models.CharField(max_length=50, blank=True)  
    establishment_name = models.CharField(max_length=50)
    license_category = models.CharField(max_length=50)
    license_type = models.CharField(max_length=50)
    license_nature = models.CharField(max_length=50)
    yearly_license_fee = models.IntegerField()

    def __str__(self): 
        return self.user_profile.username
    
    def save(self, *args, **kwargs):
     
        if not self.licensee_name:
            self.licensee_name = self.user_profile.username
        super().save(*args, **kwargs)