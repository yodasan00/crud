from rest_framework import serializers
from .models import UserDetails, LicenseDetails, LicenseDetails, MGQDetails, AddressDetails, UnitDetails, MemberDetail
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

    user_profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserDetails
        fields = ['id', 'user_profile', 'date_of_birth', 'user_status', 'phone_number']
        read_only_fields = ['user_status']
   


class MGQDetailsSerializer(serializers.ModelSerializer):
    license_details = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = MGQDetails
        fields = ['MGQ_in_BL', 'MGQ_in_LPL', 'MGQ_in_Quintal', 'deck_capacity']



class AddressDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        license_details = serializers.PrimaryKeyRelatedField(read_only=True)
        model = AddressDetails
        fields = ['police_station', 'excise_sub_division', 'ward', 'site_address', 
                  'land_details', 'block', 'road']


class UnitDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        license_details = serializers.PrimaryKeyRelatedField(read_only=True)
        model = UnitDetails
        fields = ['licensee_type', 'reg_office_address', 'pan', 'phone_number', 
                  'date_of_incorporation', 'department_office_unit', 'cin_number', 
                  'email_id', 'designation']

class MemberDetailSerializer(serializers.ModelSerializer):
    license_details = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = MemberDetail
        fields = ['id','member_status', 'member_name', 'citizenship', 'gender', 'pan_number', 
                  'mobile_number', 'email_id', 'license']



class LicenseDetailsSerializer(serializers.ModelSerializer):
    user_profile=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LicenseDetails
        fields = ['id', 'license_number', 'district_name', 'licensee_name', 'establishment_name',
                  'license_category', 'license_type', 'license_nature', 'yearly_license_fee',
                  'mgq_details', 'address_details', 'unit_details', 'members']
    
    

class OTPVerificationSerializer(serializers.ModelSerializer):
    phone_number = serializers.StringRelatedField()  

    class Meta:
        model = OTPVerification
        fields = ['id', 'phone_number', 'otp', 'created_at', 'is_verified']
        read_only_fields = ['id', 'created_at', 'is_verified'] 

    def validate_otp(self, value):
       
        if not value.isdigit() or len(value) != 4:
            raise serializers.ValidationError("Enter a valid 4-digit OTP.")
        return value
