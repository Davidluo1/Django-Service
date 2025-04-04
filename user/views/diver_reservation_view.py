from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from service.models import Driver
from user.models import Reservation

class DriverReservation(APIView):
    """Driver reservation for user"""
    permission_classes = [(IsAuthenticated)]
    
    @transaction.atomic
    def post(self,request,driver_id):
        user = request.user
        driver_qs = Driver.objects.filter(id=driver_id)
        reservation_request = request.GET.get("reserve", None)
        driver_instance = driver_qs[0]
        # Make a reservation if driver is available in the morning
        if reservation_request in ("morning",'Morning') and driver_instance.morning_shift == False:
            driver_qs.update(morning_shift=True)
            Reservation.objects.create(user=user, service_name="Driver", shift=reservation_request.lower())
            return Response({"msg":"Reservation successful!!!"}, status=200)
        elif driver_instance.morning_shift == True:
            return Response({"msg":"Driver is not available this morning"}, status=400)
        # make reservation if driver is available in the afternoon
        if reservation_request in ("afternoon","Afternoon") and driver_instance.afternoon_shift == False:
            Reservation.objects.create(user=user, service_name="Driver", shift=reservation_request.lower())
            driver_qs.update(afternoon_shift=True)
            return Response({"msg":"Reservation successful!!!"}, status=200)
        elif driver_instance.afternoon_shift == True:
            return Response({"msg":"Driver is not available this afternoon"}, status=400)
        return Response({"msg":"Driver not exist or not available at this time."}, status=400)
    
    
    @transaction.atomic
    def delete(self,request,driver_id):
        """Delete driver reservation"""
        user = request.user
        driver_qs = Driver.objects.filter(id=driver_id, user=user)
        if driver_qs.exists():
            driver_qs.delete()
            #driver_qs.update(is_deleted=True)
            return Response({"msg":"Reservation removed"}, status=200)
        return Response({"msg":"Access denied (reservation might not exist)."}, status=400)
