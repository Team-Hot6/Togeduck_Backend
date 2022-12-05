from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from workshops.models import Workshop
from workshops.serializers import WorkshopSerializer, WorkshopDetailSerializer, WorkshopDetailImageSerializer, WorkshopDetailLikesSerializer



class WorkshopView(APIView):
    def get(self, request):
        Workshops = Workshop.objects.all()
        serializer = WorkshopSerializer(Workshops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



 # 워크샵 상세페이지
class WorkshopDetailView(APIView): 

    def get(self, request, workshop_id):  
        workshop = get_object_or_404(Workshop, id=workshop_id)
        serializer = WorkshopDetailSerializer(workshop)
        return Response(serializer.data)
    
    # def post(self, request, host_id):
    #     host = get_object_or_404(Workshop, id=host_id)
    #     if request.user != host.user:     
    #         serializer = WorkshopDetailLikesSerializer(host, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.errors)

    def put(self, request, workshop_id):
        workshop = Workshop.objects.get(id=workshop_id)
        # if request.user == workshop.host:
        serializer = WorkshopDetailImageSerializer(workshop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)






            
            
            

            
            
            
            

        
        
        

        
        
        



