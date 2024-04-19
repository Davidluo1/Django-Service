from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from service.serializer import BarberRequest
from service.models import Barber
from rest_framework.permissions import IsAuthenticated


class AddBarberView(APIView):
    """Add barber"""
    
    permission_classes = [(IsAuthenticated)]
    @transaction.atomic
    def post(self,request):
        req_data = request.data
        request_data = BarberRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        barber_qs = Barber.objects.filter(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        if barber_qs.exists():
            return Response({"msg":"This barber sitter does not exist or no longer exist."}, status=400)
        barber_qs.create(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        return Response({"msg" : "Barber added successful!!!"}, status=200)
        
        
    def get(self,request):
        """Get all barbers"""
        # get all barbers
        barber_qs = Barber.objects.all()
        resp = []
        
        if barber_qs.exists():
            # store all info for each barber
            for item in barber_qs:
                resp.append({"name":item.name, "latitude":item.latitude, "longitude":item.longitude, 
                            "morning_shift":item.morning_shift, "afternoon_shift":item.afternoon_shift, 
                            "deleted":item.is_deleted})
            return Response({"Data" : resp}, status=200)
        return Response({"msg" : "No information available"}, status=400)    
    
