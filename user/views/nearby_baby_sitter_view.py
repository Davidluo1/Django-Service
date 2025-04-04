from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user.models.user import User
from service.models import BabySitter
from utils.service_distance_list import ServiceDistanceListHelper


class NearbyBabysitter(APIView):
    """Babysitter list for user"""
    permission_classes = [(IsAuthenticated)]

    def get(self,request,user_id):
        user = request.user
        user_qs = User.objects.filter(id=user_id)[0]
        user_latitude = user_qs.latitude
        user_longitude = user_qs.longitude
        # Get all baby sitters from database
        babysitter_qs = BabySitter.objects.all()
        # distance_list=[]
        if babysitter_qs:
            # approximate radius of earth in km
            # R = 6373.0
            # userlat = radians(user_latitude)
            # userlon = radians(user_longitude)
            # for babysitter in babysitter_qs:
            #     babysitterlat = radians(babysitter.latitude)
            #     babysitterlon = radians(babysitter.longitude)

            #     dlon = babysitterlon - userlon
            #     dlat = babysitterlat - userlat

            #     a = sin(dlat / 2)**2 + cos(userlat) * cos(babysitterlat) * sin(dlon / 2)**2
            #     c = 2 * atan2(sqrt(a), sqrt(1 - a))

            #     distance = R * c
            #     if distance < 1:
            #         display="meter"
            #         distance = distance*1000
            #     else:
            #         display = "km"
            #     distance_list.append({"id":babysitter.id, "name":babysitter.name, "distance":round(distance, 2)})
            # # sort distance acending order
            # babysitter_list = sorted(distance_list, key=lambda d: d['distance'])
            babysitter_list, display = ServiceDistanceListHelper(user_latitude,user_longitude, babysitter_qs)
            # distance unit check
            if display == "meter":
                return Response({"Service" : "Baby Sitter", "Measure": "meter", "babysitter" : babysitter_list}, status=200)
            return Response({"Measure": "km", "msg" : babysitter_list}, status=200)
        return Response({"msg" : "No babysitter exist"}, status=400)
    
