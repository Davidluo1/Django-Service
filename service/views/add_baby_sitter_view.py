from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from service.serializer import BabySitterRequest
from service.models import BabySitter

class AddBabySitterView(APIView):
    """Add baby sitter"""
    
    @transaction.atomic
    def post(self,request):
        req_data = request.data
        request_data = BabySitterRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        baby_sitter_qs = BabySitter.objects.filter(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        if baby_sitter_qs.exists():
            return Response({"msg":"This baby sitter does not exist or no longer exist."})
        baby_sitter_qs.create(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        return Response({"msg" : "Baby sitter added successful!!!"})
        
        