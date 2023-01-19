from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from service.models import Driver
from service.serializer import DriverRequest

class UpdateDriver(APIView):
    """Update driver"""
    
    permission_classes = [(IsAuthenticated)]
    @transaction.atomic
    def put(self,request, driver_id):
        req_data = request.data
        request_data = DriverRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        driver_qs = Driver.objects.filter(id=driver_id, is_deleted=False)
        if driver_qs.exists():
            driver_qs.update(name=req_data['name'], latitude=req_data['latitude'], longitude=req_data['longitude'], 
                           morning_shift=False, afternoon_shift=False)
            return Response({"msg" : "Driver update successful!!!"}, status=200)
        return Response({"msg" : "Driver not exist"}, status=400)

        
    @transaction.atomic
    def delete(self,request,driver_id):
        """Delete driver"""
        # find the driver and is not deleted
        driver_qs = Driver.objects.filter(id=driver_id, is_deleted=False)
        if driver_qs.exists():
            driver_qs.delete()
            #driver_qs.update(is_deleted=True)
            return Response({"msg" : "Driver delete successful!!!"}, status=200)
        return Response({"msg" : "Driver not exist"}, status=400)