from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user.models.user import User
from service.models import Chef
from utils.service_distance_list import ServiceDistanceListHelper

class NearbyChef(APIView):
    """Chef list for user"""
    permission_classes = [(IsAuthenticated)]

    def get(self,request,user_id):
        user = request.user
        user_qs = User.objects.filter(id=user_id)[0]
        user_latitude = user_qs.latitude
        user_longitude = user_qs.longitude
        # get all chefs from database
        chef_qs = Chef.objects.all()
        if chef_qs:
            chef_list, display = ServiceDistanceListHelper(user_latitude,user_longitude, chef_qs)     
            # distance unit check
            if display == "meter":
                return Response({"Service" : "Chef", "Measure": "meter", "chef" : chef_list}, status=200)
            return Response({"Measure": "km", "msg" : chef_list}, status=200)
        return Response({"msg" : "No chef exist"}, status=400)
    
    
