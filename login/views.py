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
from rest_framework.authtoken.models import Token
from django.http import JsonResponse




def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            
            user.user_details.user_status = True
            user.user_details.save() 

            token, created = Token.objects.get_or_create(user=user)
            
           
            return JsonResponse({"token": token.key}, status=200)
        
        else:
           
            messages.error(request, "Invalid username or password.")
            return redirect("login")  

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
    def post(self, request):
        phone_number = request.data.get('phone_number')
        
        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
        
     
        try:
            user_details = UserDetails.objects.get(phone_number=phone_number)
        except UserDetails.DoesNotExist:
            return Response({"error": "Phone number not found."}, status=status.HTTP_404_NOT_FOUND)

       
        otp_code = f"{random.randint(1000, 9999)}"

       
        otp_instance = OTPVerification.objects.create(phone_number=user_details, otp=otp_code)

        
        email = user_details.user_profile.email  
        
        if email:
            subject = "Your OTP Code"
            message = f"Dear  {user_details.user_profile.username},\n\nYour OTP is: {otp_code}\n\nThis code will expire in 5 minutes."
            from_email = 'pushkarraj192003l@gmail.com' 
            recipient_list = [email] 

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

       
        serializer = OTPVerificationSerializer(otp_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyOTPView(APIView):
   
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        
        if not phone_number :
            return Response({"error": "Phone numbe  required."}, status=status.HTTP_400_BAD_REQUEST)
        if not otp:
            return Response({"error": "OTP is required."}, status=status.HTTP_400_BAD_REQUEST)
        
      
        try:
            otp_instance = OTPVerification.objects.filter(
                phone_number__phone_number=phone_number, otp=otp, is_verified=False
            ).latest('created_at')
            
          
            
            if timezone.now() - otp_instance.created_at > timedelta(minutes=5):
                return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)
            
           
            otp_instance.is_verified = True
            otp_instance.save()

            user_details = otp_instance.phone_number
            user_details.user_status = True
            user_details.save()

            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK) 

           
        
        except OTPVerification.DoesNotExist:
            return Response({"error": "Invalid or expired OTP.(th)"}, status=status.HTTP_400_BAD_REQUEST)
