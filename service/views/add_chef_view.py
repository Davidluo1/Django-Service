from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from service.serializer import ChefRequest
from service.models import Chef

class AddChefView(APIView):
    """Add chef"""
    
    @transaction.atomic
    def post(self,request):
        req_data = request.data
        request_data = ChefRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        chef_qs = Chef.objects.filter(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        if chef_qs.exists():
            return Response({"msg":"This chef sitter does not exist or no longer exist."})
        chef_qs.create(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        return Response({"msg" : "Chef added successful!!!"})

        