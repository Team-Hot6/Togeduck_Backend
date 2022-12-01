from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

# 채팅방 보기 view - ing
class LobbyView(APIView):
    def get(self, request):
        print('test')
        return Response(request.data, status=status.HTTP_200_OK)