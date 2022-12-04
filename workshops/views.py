from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from workshops.models import Workshop
from workshops.serializers import WorkshopSerializer, WorkshopDetailSerializer, WorkshopDetailImageSerializer, WorkshopDetailLikesSerializer



class WorkshopDetailView(APIView):  # 워크샵 상세페이지

    def get(self, request, nickname):  
        workshop = get_object_or_404(Workshop, nickname=nickname)
        serializer = WorkshopDetailSerializer(workshop)
        return Response(serializer.data)
    
    def post(self, request, host_id):
        host = get_object_or_404(Workshop, id=host_id)
        if request.user != host.user:     
            serializer = WorkshopDetailLikesSerializer(host, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

    def put(self, request, host_id):
        host = get_object_or_404(Workshop, id=host_id)
        if request.user == host.user:
            serializer = WorkshopDetailImageSerializer(host, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)






            
            
            

            
            
            
            

        
        
        

        
        
        


# Create your views here.
class WorkshopView(APIView):
    def get(self, request):
        Workshops = Workshop.objects.all()
        serializer = WorkshopSerializer(Workshops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
