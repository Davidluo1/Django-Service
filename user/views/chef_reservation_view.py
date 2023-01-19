from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from service.models import Chef
from user.models import Reservation

class ChefReservation(APIView):
    """Chef reservation for user"""
    permission_classes = [(IsAuthenticated)]
    
    @transaction.atomic
    def post(self,request,chef_id):
        user = request.user
        chef_qs = Chef.objects.filter(id=chef_id)
        reservation_request = request.GET.get("reserve", None)
        chef_instance = chef_qs[0]
        # make reservation if chef is available in morning
        if reservation_request in ("morning",'Morning') and chef_instance.morning_shift == False:
            chef_qs.update(morning_shift=True)
            Reservation.objects.create(user=user, service_name="Chef", shift=reservation_request.lower())
            return Response({"msg":"Reservation successful!!!"}, status=200)
        elif chef_instance.morning_shift == True:
            return Response({"msg":"Chef is not available this morning"}, status=400)
        # make reservation if chef is available in afternoon
        if reservation_request in ("afternoon","Afternoon") and chef_instance.afternoon_shift == False:
            Reservation.objects.create(user=user, service_name="Chef", shift=reservation_request.lower())
            chef_qs.update(afternoon_shift=True)
            return Response({"msg":"Reservation successful!!!"}, status=200)
        elif chef_instance.afternoon_shift == True:
            return Response({"msg":"Chef is not available this afternoon"}, status=400)
        return Response({"msg":"Chef not exist or not available at this time."}, status=400)
    
    

    @transaction.atomic
    def delete(self,request,chef_id):
        """Delete chef reservation"""
        user = request.user
        chef_qs = Chef.objects.filter(id=chef_id, user=user)
        if chef_qs.exists():
            chef_qs.delete()
            #chef_qs.update(is_deleted=True)
            return Response({"msg":"Reservation removed"}, status=200)
        return Response({"msg":"Access denied (reservation might not exist)."}, status=400)