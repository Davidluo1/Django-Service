from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from service.models import BabySitter
from user.models import Reservation

class BabySitterReservation(APIView):
    """Babysitter reservation for user"""
    permission_classes = [(IsAuthenticated)]
    
    @transaction.atomic
    def post(self,request,babysitter_id):
        user = request.user
        babysitter_qs = BabySitter.objects.filter(id=babysitter_id)
        reservation_request = request.GET.get("reserve", None)
        babysitter_instance = babysitter_qs[0]
        
        # Make reservation if babysitter is available in morning
        if reservation_request in ("morning",'Morning') and babysitter_instance.morning_shift == False:
            babysitter_qs.update(morning_shift=True)
            Reservation.objects.create(user=user, service_name="Baby sitter", shift=reservation_request.lower())
            return Response({"msg":"Reservation successful!!!"}, status=200)
        elif babysitter_instance.morning_shift == True:
            return Response({"msg":"Baby sitter is not available this morning"}, status=400)
            
        # make reservation if babysitter is available in the afternoon
        if reservation_request in ("afternoon", "Afternoon") and babysitter_instance.afternoon_shift == False:
            Reservation.objects.create(user=user, service_name="Baby sitter", shift=reservation_request.lower())
            babysitter_qs.update(afternoon_shift=True)
            return Response({"msg":"Reservation successful!!!"}, status=200)
        elif babysitter_instance.afternoon_shift == True:
            return Response({"msg":"Baby sitter is not available this afternoon"}, status=400)
        return Response({"msg":"Baby sitter not exist or not available at this time."}, status=400)
    
    

    @transaction.atomic
    def delete(self,request,babysitter_id):
        """Delete baby sitter reservation"""
        user = request.user
        babysitter_qs = BabySitter.objects.filter(id=babysitter_id, user=user)
        
        if babysitter_qs.exists():
            babysitter_qs.delete()
            #babysitter_qs.update(is_deleted=True)
            return Response({"msg":"Reservation removed"}, status=200)
        return Response({"msg":"Access denied (reservation might not exist)."}, status=400)
