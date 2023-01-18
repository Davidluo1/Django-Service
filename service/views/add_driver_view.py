from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from service.serializer import DriverRequest
from service.models import Driver
from rest_framework.permissions import IsAuthenticated

class AddDriverView(APIView):
    """Add driver"""
    
    permission_classes = [(IsAuthenticated)]
    @transaction.atomic
    def post(self,request):
        req_data = request.data
        request_data = DriverRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        driver_qs = Driver.objects.filter(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        if driver_qs.exists():
            return Response({"msg":"This driver sitter does not exist or no longer exist."}, status=400)
        driver_qs.create(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        return Response({"msg" : "Driver added successful!!!"}, status=200)
        
        
        
    def get(self,request):
        """Get all drivers"""
        driver_qs = Driver.objects.all()
        resp = []
        if driver_qs.exists():
            for item in driver_qs:
                resp.append({"name":item.name, "latitude":item.latitude, "longitude":item.longitude, 
                            "morning_shift":item.morning_shift, "afternoon_shift":item.afternoon_shift, 
                            "deleted":item.is_deleted})
            return Response({"Data" : resp}, status=200)
        return Response({"msg" : "No information available"}, status=400) 