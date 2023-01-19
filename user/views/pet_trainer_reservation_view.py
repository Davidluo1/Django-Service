from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from service.models import PetTrainer
from user.models import Reservation

class PetTrainerReservation(APIView):
    """Pet trainer reservation for user"""
    permission_classes = [(IsAuthenticated)]
    
    @transaction.atomic
    def post(self,request,pettrainer_id):
        user = request.user
        pettrainer_qs = PetTrainer.objects.filter(id=pettrainer_id)
        reservation_request = request.GET.get("reserve", None)
        pettrainer_instance = pettrainer_qs[0]
        # make reservation if pettrainer is available in morning
        if reservation_request in ("morning",'Morning') and pettrainer_instance.morning_shift == False:
            pettrainer_qs.update(morning_shift=True)
            Reservation.objects.create(user=user, service_name="Pet trainer", shift=reservation_request.lower())
            return Response({"msg":"Reservation successful!!!"}, status=200)
        elif pettrainer_instance.morning_shift == True:
            return Response({"msg":"Pet trainer is not available this morning"}, status=400)
        # make reservation if pettrainer is available in afternoon
        if reservation_request in ("afternoon","Afternoon") and pettrainer_instance.afternoon_shift == False:
            Reservation.objects.create(user=user, service_name="Pet trainer", shift=reservation_request.lower())
            pettrainer_qs.update(afternoon_shift=True)
            return Response({"msg":"Reservation successful!!!"}, status=200)
        elif pettrainer_instance.afternoon_shift == True:
            return Response({"msg":"Pet trainer is not available this afternoon"}, status=400)
        return Response({"msg":"Pet trainer not exist or not available at this time."}, status=400)
    
    
    @transaction.atomic
    def delete(self,request,pettrainer_id):
        """Delete pet trainer reservation"""
        user = request.user
        pettrainer_qs = PetTrainer.objects.filter(id=pettrainer_id, user=user)
        if pettrainer_qs.exists():
            pettrainer_qs.delete()
            #pettrainer_qs.update(is_deleted=True)
            return Response({"msg":"Reservation removed"}, status=200)
        return Response({"msg":"Access denied (reservation might not exist)."}, status=400)
    
    
