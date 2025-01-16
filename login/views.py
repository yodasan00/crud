from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.serializers import UserDetailsSerializer,LicenseDetailsSerializer,userSerializer
from .models import UserDetails,LicenseDetails,OTPVerification
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OTPVerificationSerializer



def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
      
        if not User.objects.filter(username=username).exists():
            print(request, "Username is incorrect. Please try again.")
            return render(request, 'registration/log.html')
        
     
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "registration/sucessful.html")
        else:
           print(request, "Password is incorrect. Please try again.")
           return render(request, 'registration/log.html')
    else:
        return render(request, 'registration/log.html')

@login_required

def User_page(request):
    return render(request,"registration/sucessful.html")

class UserDetailsSerializerViewset(viewsets.ModelViewSet):
    serializer_class = UserDetailsSerializer
    queryset = UserDetails.objects.all()
   # authentication_classes=(TokenAuthentication,)

class LicenseDetailsSerializerViewset( viewsets.ModelViewSet):
    serializer_class = LicenseDetailsSerializer
    queryset = LicenseDetails.objects.all()
   # authentication_classes=(TokenAuthentication,)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializer
   


class CreateOTPView(APIView):
    """
    Handles OTP generation for a given phone number.
    """
    def post(self, request):
        phone_number = request.data.get('phone_number')
        
        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the phone number exists in UserDetails
        try:
            user_details = UserDetails.objects.get(phone_number=phone_number)
        except UserDetails.DoesNotExist:
            return Response({"error": "Phone number not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Generate OTP (you can replace this with a more secure generator)
        import random
        otp_code = f"{random.randint(1000, 9999)}"
        
        # Create an OTPVerification record
        otp_instance = OTPVerification.objects.create(phone_number=user_details, otp=otp_code)
        
        # Serialize and return the OTP instance (you might exclude the OTP in production for security)
        serializer = OTPVerificationSerializer(otp_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyOTPView(APIView):
    """
    Handles OTP verification for a given phone number and OTP.
    """
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        
        if not phone_number or not otp:
            return Response({"error": "Phone number and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify the OTP
        try:
            otp_instance = OTPVerification.objects.filter(
                phone_number__phone_number=phone_number, otp=otp, is_verified=False
            ).latest('created_at')
            
            # Check if the OTP is within the valid time window
            from datetime import timedelta
            from django.utils import timezone
            if timezone.now() - otp_instance.created_at > timedelta(minutes=10):
                return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Mark OTP as verified
            otp_instance.is_verified = True
            otp_instance.save()
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        
        except OTPVerification.DoesNotExist:
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
