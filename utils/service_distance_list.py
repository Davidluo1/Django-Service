from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from math import sin, cos, sqrt, atan2, radians


def ServiceDistanceListHelper(user_latitude, user_longitude, service_qs, display="km"):
    distance_list=[]
    # approximate radius of earth in km
    R = 6373.0
    userlat = radians(user_latitude)
    userlon = radians(user_longitude)
    for babysitter in service_qs:
        babysitterlat = radians(babysitter.latitude)
        babysitterlon = radians(babysitter.longitude)

        dlon = babysitterlon - userlon
        dlat = babysitterlat - userlat

        a = sin(dlat / 2)**2 + cos(userlat) * cos(babysitterlat) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        if distance < 1:
            display="meter"
            distance = distance*1000

        distance_list.append({"id":babysitter.id, "name":babysitter.name, "distance":round(distance, 2)})
    # sort distance acending order
    service_list = sorted(distance_list, key=lambda d: d['distance'])
    return service_list, display
    
