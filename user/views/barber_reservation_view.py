from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from service.models import Barber
from user.models import Reservation

class BarberReservation(APIView):
    """Barber reservation for user"""
    permission_classes = [(IsAuthenticated)]
    
    @transaction.atomic
    def post(self,request,barber_id):
        user = request.user
        barber_qs = Barber.objects.filter(id=barber_id)
        reservation_request = request.GET.get("reserve", None)
        barber_instance = barber_qs[0]
        
        # Make a reservation if a barber is available in the morning
        if reservation_request in ("morning",'Morning') and barber_instance.morning_shift == False:
            barber_qs.update(morning_shift=True)
            Reservation.objects.create(user=user, service_name="Barber", shift=reservation_request.lower())
            return Response({"msg":"Reservation successful!!!"}, status=200)
        elif barber_instance.morning_shift == True:
            return Response({"msg":"Barber is not available this morning"}, status=400)
            
        # Make a reservation if a barber is available in the afternoon
        if reservation_request in ("afternoon","Afternoon") and barber_instance.afternoon_shift == False:
            Reservation.objects.create(user=user, service_name="Barber", shift=reservation_request.lower())
            barber_qs.update(afternoon_shift=True)
            return Response({"msg":"Reservation successful!!!"}, status=200)
        elif barber_instance.afternoon_shift == True:
            return Response({"msg":"Barber is not available this afternoon"}, status=400)
        return Response({"msg":"Barber not exist or not available at this time."}, status=400)
    
    

    @transaction.atomic
    def delete(self,request,baber_id):
        """Delete a barber reservation"""
        user = request.user
        baber_qs = Barber.objects.filter(id=baber_id, user=user)
        
        if baber_qs.exists():
            baber_qs.delete()
            #baber_qs.update(is_deleted=True)
            return Response({"msg":"Reservation removed"}, status=200)
        return Response({"msg":"Access denied (reservation might not exist)."}, status=400)
