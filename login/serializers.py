from rest_framework import serializers
from .models import UserDetails, LicenseDetails
from django.contrib.auth.models import User

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Serializer for UserDetails
class UserDetailsSerializer(serializers.ModelSerializer):
    user_profile = userSerializer(many=False)
    class Meta:
        model = UserDetails
        fields = ['id', 'user_profile', 'date_of_birth', 'user_status', 'phone_number']

# Serializer for LicenseDetails
class LicenseDetailsSerializer(serializers.ModelSerializer):
    user_profile = userSerializer(many=False)
    class Meta:
        model = LicenseDetails
        fields = ['id', 'user_profile', 'license_number', 'district_name', 'licensee_name', 'establishment_name', 
                  'license_category', 'license_type', 'license_nature', 'yearly_license_fee']
