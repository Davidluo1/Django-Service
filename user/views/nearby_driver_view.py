from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user.models.user import User
from service.models import Driver
from utils.service_distance_list import ServiceDistanceListHelper


class NearbyDriver(APIView):
    """Driver list for user"""
    permission_classes = [(IsAuthenticated)]
    
    def get(self,request,user_id):
        user = request.user
        user_qs = User.objects.filter(id=user_id)[0]
        user_latitude = user_qs.latitude
        user_longitude = user_qs.longitude
        # Get all drivers from database
        driver_qs = Driver.objects.all()
        if driver_qs:
            driver_list, display = ServiceDistanceListHelper(user_latitude,user_longitude, driver_qs)   
            # distance unit check
            if display == "meter":
                return Response({"Service" : "Driver", "Measure": "meter", "driver" : driver_list}, status=200)
            return Response({"Measure": "km", "msg" : driver_list}, status=200)
        return Response({"msg" : "No driver exist"}, status=400)
