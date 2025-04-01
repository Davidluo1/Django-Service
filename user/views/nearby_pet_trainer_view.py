from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user.models.user import User
from service.models import PetTrainer
from utils.service_distance_list import ServiceDistanceListHelper


class NearbyPetTrainer(APIView):
    """Pet trainer list for user"""
    permission_classes = [(IsAuthenticated)]

    def get(self,request,user_id):
        user = request.user
        user_qs = User.objects.filter(id=user_id)[0]
        user_latitude = user_qs.latitude
        user_longitude = user_qs.longitude
        # Get all pet trainers from database
        pet_trainer_qs = PetTrainer.objects.all()
        if pet_trainer_qs:
            pet_trainer_list, display = ServiceDistanceListHelper(user_latitude,user_longitude, pet_trainer_qs)    
            # Distance unit check
            if display == "meter":
                return Response({"Service" : "Pet trainer", "Measure": "meter", "Trainer" : pet_trainer_list}, status=200)
            return Response({"Measure": "km", "msg" : pet_trainer_list}, status=200)
        return Response({"msg" : "No pet trainer exist"}, status=400)
