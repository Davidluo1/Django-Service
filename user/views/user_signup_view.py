from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializer import SignUpRequest, UserSerializer
import random
from django.db import transaction

class UserSignUpView(APIView):
    """User SignUp View class"""
    
    @transaction.atomic
    def post(self,request):
        req_data = request.data
        request_data = SignUpRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        
        # Resolve duplicate email/phone number by returning an error response
        if User.objects.filter(email = req_data["email"]).exists():
            return Response({"msg" : "Email already exists"}, status = 400)
        if User.objects.filter(contact_number = req_data["contact_number"]).exists():
            return Response({"msg" : "Phone already being signed up to other user account"}, status = 400)
        # Create an user table element with password encrypted
        user_instance = UserSerializer.create(req_data)
        # Create an random otp value for the user
        # OtpUser.objects.create(otp_value = random.randint(100000, 999999), user= user_instance)
        return Response({"msg" : "Sign up successful!!!"})
        
