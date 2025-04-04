from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user.models.user import User
from service.models import Barber
from utils.service_distance_list import ServiceDistanceListHelper


class NearbyBarber(APIView):
    """Barber list for user"""
    permission_classes = [(IsAuthenticated)]
    
    def get(self,request,user_id):
        user = request.user
        user_qs = User.objects.filter(id=user_id)[0]
        user_latitude = user_qs.latitude
        user_longitude = user_qs.longitude
        # Get all barbers from database
        barber_qs = Barber.objects.all()
        # distance_list=[]
        if barber_qs:
            # Approximate radius of earth in km
            # R = 6373.0
            # userlat = radians(user_latitude)
            # userlon = radians(user_longitude)
            # for barber in barber_qs:
            #     barberlat = radians(barber.latitude)
            #     baberlon = radians(barber.longitude)

            #     dlon = baberlon - userlon
            #     dlat = barberlat - userlat

            #     a = sin(dlat / 2)**2 + cos(userlat) * cos(barberlat) * sin(dlon / 2)**2
            #     c = 2 * atan2(sqrt(a), sqrt(1 - a))

            #     distance = R * c
            #     if distance < 1:
            #         display="meter"
            #         distance = distance*1000
            #     else:
            #         display = "km"
            #     distance_list.append({"id":barber.id, "name":barber.name, "distance":round(distance, 2)})
            # # sort distance acending order
            # barber_list = sorted(distance_list, key=lambda d: d['distance'])
            barber_list, display = ServiceDistanceListHelper(user_latitude,user_longitude, barber_qs)    
            # Distance unit check
            if display == "meter":
                return Response({"Service" : "Barber", "Measure": "meter", "Barber" : barber_list}, status=200)
            return Response({"Measure": "km", "msg" : barber_list}, status=200)
        return Response({"msg" : "No barber exist"}, status=400)
