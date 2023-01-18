from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from service.models import PetTrainer
from service.serializer import PetTrainerRequest

class UpdatePetTrainer(APIView):
    """Update pettrainer"""
    
    permission_classes = [(IsAuthenticated)]
    @transaction.atomic
    def put(self,request, pettrainer_id):
        req_data = request.data
        request_data = PetTrainerRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        pettrainer_qs = PetTrainer.objects.filter(id=pettrainer_id, is_deleted=False)
        if pettrainer_qs.exists():
            pettrainer_qs.update(name=req_data['name'], latitude=req_data['latitude'], longitude=req_data['longitude'], 
                           morning_shift=False, afternoon_shift=False)
            return Response({"msg" : "Pet trainer update successful!!!"}, status=200)
        return Response({"msg" : "Pet trainer not exist"}, status=400)

    
    
    @transaction.atomic
    def delete(self,request,pet_trainer_id):
        pet_trainer_qs = PetTrainer.objects.filter(id=pet_trainer_id, is_deleted=False)
        if pet_trainer_qs.exists():
            pet_trainer_qs.delete()
            #pet_trainer_qs.update(is_deleted=True)
            return Response({"msg" : "Pet trainer delete successful!!!"}, status=200)
        return Response({"msg" : "Pet trainer not exist"}, status=400)