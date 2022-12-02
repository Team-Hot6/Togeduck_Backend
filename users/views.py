from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from users.models import User
from users.serializers import UserProfileSerializer



class UserProfileView(APIView): # 마이페이지 화면
    def get(self, request, nickname):  
        user = get_object_or_404(User, nickname=nickname)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)









        
