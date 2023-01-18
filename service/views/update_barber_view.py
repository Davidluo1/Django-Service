from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from service.models import Barber
from service.serializer import BarberRequest

class UpdateBarber(APIView):
    """Update barber"""
    
    permission_classes = [(IsAuthenticated)]
    @transaction.atomic
    def put(self,request, barber_id):
        req_data = request.data
        request_data = BarberRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        barber_qs = Barber.objects.filter(id=barber_id, is_deleted=False)
        if barber_qs.exists():
            barber_qs.update(name=req_data['name'], latitude=req_data['latitude'], longitude=req_data['longitude'], 
                           morning_shift=False, afternoon_shift=False)
            return Response({"msg" : "Barber update successful!!!"}, status=200)
        return Response({"msg" : "Barber not exist"}, status=400)

        
    @transaction.atomic
    def delete(self,request,barber_id):
        barber_qs = Barber.objects.filter(id=barber_id, is_deleted=False)
        if barber_qs.exists():
            barber_qs.delete()
            #barber_qs.update(is_deleted=True)
            return Response({"msg" : "Barber delete successful!!!"}, status=200)
        return Response({"msg" : "Barber not exist"}, status=400)