from rest_framework import serializers
from .models import UserDetails, LicenseDetails
from django.contrib.auth.models import User
from .models import OTPVerification



class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserDetailsSerializer(serializers.ModelSerializer):
    #user_profile = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Reference to the User model
    user_profile=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = UserDetails
        fields = ['id', 'user_profile', 'date_of_birth', 'user_status', 'phone_number']
   


class LicenseDetailsSerializer(serializers.ModelSerializer):
    user_profile=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = LicenseDetails
        fields = ['id', 'user_profile', 'license_number', 'district_name', 'licensee_name', 'establishment_name', 
                  'license_category', 'license_type', 'license_nature', 'yearly_license_fee']
   


class OTPVerificationSerializer(serializers.ModelSerializer):
    phone_number = serializers.StringRelatedField()  

    class Meta:
        model = OTPVerification
        fields = ['id', 'phone_number', 'otp', 'created_at', 'is_verified']
        read_only_fields = ['id', 'created_at', 'is_verified'] # These fields are read-only

    def validate_otp(self, value):
       
        if not value.isdigit() or len(value) != 4:
            raise serializers.ValidationError("Enter a valid 4-digit OTP.")
        return value
