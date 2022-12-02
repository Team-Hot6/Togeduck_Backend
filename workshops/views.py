from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from workshops.models import Workshop
from workshops.serializers import WorkshopSerializer

# Create your views here.
class WorkshopView(APIView):
    def get(self, request):
        Workshops = Workshop.objects.all()
        serializer = WorkshopSerializer(Workshops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)