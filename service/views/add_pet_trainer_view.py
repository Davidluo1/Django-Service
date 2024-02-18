from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from service.serializer import PetTrainerRequest
from service.models import PetTrainer
from rest_framework.permissions import IsAuthenticated

class AddPetTrainer(APIView):
    """Add pet trainer"""
    
    permission_classes = [(IsAuthenticated)]
    @transaction.atomic
    def post(self,request):
        req_data = request.data
        request_data = PetTrainerRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        pettrainer_qs = PetTrainer.objects.filter(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        if pettrainer_qs.exists():
            return Response({"msg":"This pet trainer sitter does not exist or no longer exist."}, status=400)
        pettrainer_qs.create(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        return Response({"msg" : "Pet trainer added successful!!!"}, status=200)

    
    def get(self,request):
        """Get all pet trainers"""
        # get all pet trainer
        pettrainer_qs = PetTrainer.objects.all()
        resp = []
        if pettrainer_qs.exists():
            # store all info for every pet trainer
            for item in pettrainer_qs:
                resp.append({"name":item.name, "latitude":item.latitude, "longitude":item.longitude, 
                            "morning_shift":item.morning_shift, "afternoon_shift":item.afternoon_shift, 
                            "deleted":item.is_deleted})
            return Response({"Data" : resp}, status=200)
        return Response({"msg" : "No information available"}, status=400) 
