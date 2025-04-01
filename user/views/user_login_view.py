from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializer.user_login_request import LoginRequest
from user.models.user import User
from rest_framework.authtoken.models import Token
from django.db import transaction


class UserLoginView(APIView):
    """Login functionality for user"""
    
    @transaction.atomic
    def post(self,request):
        req_data = request.data
        request_data = LoginRequest(data=req_data)
        # _ when not sure what input 
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        email = req_data['email']
        password = req_data['password']
        user_qs = User.objects.filter(email = email)
        if user_qs.exists():
            user_instance = user_qs[0]
            # Bool check is the account activated
            if user_instance.otp_verify:
                # bool password check
                password_match = user_instance.check_password(password)
                if password_match:
                    # create a token key for the user once logged in
                    token, created = Token.objects.get_or_create(user=user_instance)
                    #print(token)
                    return Response({"msg" : "Login successful!!!"})
                else:
                    return Response({"msg" : "Incorrect password"}, status=400)
            else:
                return Response({"msg" : "Account not activated"}, status=400)
        else:
            return Response({"msg" : "Does not match the record"}, status=400)
