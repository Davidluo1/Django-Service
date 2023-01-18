from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from service.models import Chef
from service.serializer import ChefRequest

class UpdateChef(APIView):
    """Update chef"""
    
    permission_classes = [(IsAuthenticated)]
    @transaction.atomic
    def put(self,request, chef_id):
        req_data = request.data
        request_data = ChefRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        chef_qs = Chef.objects.filter(id=chef_id, is_deleted=False)
        if chef_qs.exists():
            chef_qs.update(name=req_data['name'], latitude=req_data['latitude'], longitude=req_data['longitude'], 
                           morning_shift=False, afternoon_shift=False)
            return Response({"msg" : "Chef update successful!!!"}, status=200)
        return Response({"msg" : "Chef not exist"}, status=400)

        
    @transaction.atomic
    def delete(self,request,chef_id):
        chef_qs = Chef.objects.filter(id=chef_id, is_deleted=False)
        if chef_qs.exists():
            chef_qs.delete()
            #chef_qs.update(is_deleted=True)
            return Response({"msg" : "Chef delete successful!!!"}, status=200)
        return Response({"msg" : "Chef not exist"}, status=400)