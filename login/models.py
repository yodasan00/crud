from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import RegexValidator
from django.db import models
from datetime import timedelta
from django.utils import timezone


phone_number_validator = RegexValidator(
    regex=r'^\d{10}$', 
    message="Enter a valid 10-digit phone number."
)
validate_4_digit_otp = RegexValidator(
    regex=r'^\d{4}$',
    message="Enter a valid 4-digit OTP."
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




class OTPVerification(models.Model):
    phone_number = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="otp_verifications")
    otp = models.CharField(max_length=4, validators=[validate_4_digit_otp])
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.phone_number.phone_number}"

    def save(self, *args, **kwargs):
       
        if OTPVerification.objects.filter(
            phone_number=self.phone_number,
            is_verified=False,
            created_at__gte=timezone.now() - timedelta(minutes=1)
        ).exists():
            raise ValueError("An active OTP already exists for this phone number.")

        \
        super().save(*args, **kwargs)

    @staticmethod
    def verify_otp(phone_number, otp):
  
        try:
            otp_record = OTPVerification.objects.filter(
                phone_number__phone_number=phone_number,
                otp=otp,
                is_verified=False,  
            ).latest('created_at')

            
            if timezone.now() - otp_record.created_at > timedelta(minutes=1):
                return False
            

      
            otp_record.is_verified = True
            otp_record.save()
            return True
        except OTPVerification.DoesNotExist:
            return False
