from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.serializers import UserDetailsSerializer,LicenseDetailsSerializer,userSerializer,OTPVerificationSerializer
from .models import UserDetails,LicenseDetails,OTPVerification
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
import random
from django.core.mail import send_mail



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
    Handles OTP generation for a given phone number and sends OTP to the associated email.
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

        # Generate OTP
        otp_code = f"{random.randint(1000, 9999)}"

        # Create an OTPVerification record
        otp_instance = OTPVerification.objects.create(phone_number=user_details, otp=otp_code)

        # Send OTP via email (using the email associated with User model)
        email = user_details.user_profile.email  # Get email from User model
        
        if email:
            subject = "Your OTP Code"
            message = f"Dear {user_details.user_profile.username},\n\nYour OTP is: {otp_code}\n\nThis code will expire in 10 minutes."
            from_email = 'pushkarraj192003l@gmail.com'  # Your email for sending OTP
            recipient_list = [email]  # Recipient email

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Serialize and return the OTP instance
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
            
            if timezone.now() - otp_instance.created_at > timedelta(minutes=1):
                return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Mark OTP as verified
            otp_instance.is_verified = True
            otp_instance.save()
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        
        except OTPVerification.DoesNotExist:
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
