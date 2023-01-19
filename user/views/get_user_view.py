from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models.user import User


class UserList(APIView):
    """Dispaly user list"""
    
    def get(self,request):
        # get all users from database
        user_list = User.objects.all()
        resp=[]
        total=0
        if user_list:
            # count total number of users and store them into a list
            for data in user_list:
                total+=1
                resp.append({"id":data.id, "name":data.name, "contact":data.contact_number,
                            "email":data.email, "latitude":data.latitude, "longitude":data.longitude})
            return Response({"Total users":total, "Data list" : resp}, status=400)
        return Response({"msg" : "User not found"}, status=400)