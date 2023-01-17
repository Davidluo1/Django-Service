from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from service.serializer import PetTrainerRequest
from service.models import PetTrainer

class AddPetTrainer(APIView):
    """Add pet trainer"""
    
    @transaction.atomic
    def post(self,request):
        req_data = request.data
        request_data = PetTrainerRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        pet_trainer_qs = PetTrainer.objects.filter(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        if pet_trainer_qs.exists():
            return Response({"msg":"This pet trainer sitter does not exist or no longer exist."})
        pet_trainer_qs.create(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        return Response({"msg" : "Pet trainer added successful!!!"})

        