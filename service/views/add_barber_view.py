from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from service.serializer import BarberRequest
from service.models import Barber


class AddBarberView(APIView):
    """Add barber"""
    
    @transaction.atomic
    def post(self,request):
        req_data = request.data
        request_data = BarberRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        barber_qs = Barber.objects.filter(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        if barber_qs.exists():
            return Response({"msg":"This barber sitter does not exist or no longer exist."})
        barber_qs.create(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        return Response({"msg" : "Barber added successful!!!"})
        