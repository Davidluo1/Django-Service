from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from service.serializer import BabySitterRequest
from service.models import BabySitter
from rest_framework.permissions import IsAuthenticated


class AddBabySitterView(APIView):
    """Add baby sitter"""
    
    permission_classes = [(IsAuthenticated)]
    @transaction.atomic
    def post(self,request):
        req_data = request.data
        request_data = BabySitterRequest(data=req_data)
        _ = request_data.is_valid(raise_exception=True)
        req_data = request_data.validated_data
        babysitter_qs = BabySitter.objects.filter(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        if babysitter_qs.exists():
            return Response({"msg":"This baby sitter does not exist or no longer exist."}, status=400)
        babysitter_qs.create(name=req_data['name'], 
                                                   longitude=req_data['longitude'], latitude=req_data['latitude'])
        return Response({"msg" : "Baby sitter added successful!!!"}, status=200)
        
        
    def get(self,request):
        """Get all baby sitters"""
        # get all baby sitter
        babysitter_qs = BabySitter.objects.all()
        resp = []
        if babysitter_qs.exists():
            # store all info for each baby sitter
            for item in babysitter_qs:
                resp.append({"name":item.name, "latitude":item.latitude, "longitude":item.longitude, 
                            "morning_shift":item.morning_shift, "afternoon_shift":item.afternoon_shift, 
                            "deleted":item.is_deleted})
            return Response({"Data" : resp}, status=200)
        return Response({"msg" : "No information available"}, status=400)
    
    
