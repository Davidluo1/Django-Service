from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from service.models import BabySitter
from service.serializer import BabySitterRequest

class UpdateBabySitter(APIView):
    """Update babysitter"""
    
    permission_classes = [(IsAuthenticated)]
    @transaction.atomic
    def put(self,request, babysitter_id):
        req_data = request.data
        request_data = BabySitterRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        babysitter_qs = BabySitter.objects.filter(id=babysitter_id, is_deleted=False)
        if babysitter_qs.exists():
            babysitter_qs.update(name=req_data['name'], latitude=req_data['latitude'], longitude=req_data['longitude'], 
                           morning_shift=False, afternoon_shift=False)
            return Response({"msg" : "Babysitter update successful!!!"}, status=200)
        return Response({"msg" : "Babysitter not exist"}, status=400)

        
    @transaction.atomic
    def delete(self,request, babysitter_id):
        babysitter_qs = BabySitter.objects.filter(id=babysitter_id, is_deleted=False)
        if babysitter_qs.exists():
            babysitter_qs.delete()
            # babysitter_qs.update(is_deleted=True)
            return Response({"msg" : "Babysitter delete successful!!!"}, status=200)
        return Response({"msg" : "Baby sitter not exist"}, status=400)
    
    
    