from django.db import models
from django.contrib.auth.models import User  # Import the built-in User model
from django.core.validators import RegexValidator
from django.db import models

# Phone number validator for exactly 10 digits
phone_number_validator = RegexValidator(
    regex=r'^\d{10}$',  # Matches exactly 10 digits
    message="Enter a valid 10-digit phone number."
)

class UserDetails(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to auth_user table
    date_of_birth = models.DateField(default=None)
    user_status = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=10, validators=[phone_number_validator],unique=True)

    def __str__(self): 
        return self.user_profile.username


# LicenseDetails linked to the built-in User model
class LicenseDetails(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to auth_user table
    license_number = models.CharField(max_length=50,unique=True)
    district_name = models.CharField(max_length=50)
    licensee_name = models.CharField(max_length=50, blank=True)  # Optional field, can be set dynamically
    establishment_name = models.CharField(max_length=50)
    license_category = models.CharField(max_length=50)
    license_type = models.CharField(max_length=50)
    license_nature = models.CharField(max_length=50)
    yearly_license_fee = models.IntegerField()

    def __str__(self): 
        return self.user_profile.username
    
    def save(self, *args, **kwargs):
        # If licensee_name is not already set, set it dynamically from user_profile
        if not self.licensee_name:
            self.licensee_name = self.user_profile.username
        super().save(*args, **kwargs)