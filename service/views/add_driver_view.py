from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from service.serializer import DriverRequest
from service.models import Driver

class AddDriverView(APIView):
    """Add driver"""
    
    @transaction.atomic
    def post(self,request):
        req_data = request.data
        request_data = DriverRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        driver_qs = Driver.objects.filter(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        if driver_qs.exists():
            return Response({"msg":"This driver sitter does not exist or no longer exist."})
        driver_qs.create(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        return Response({"msg" : "Driver added successful!!!"})
        