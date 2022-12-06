from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from workshops.models import Workshop, WorkshopApply
from workshops.serializers import WorkshopListSerializer, WorkshopSerializer, WorkshopCreateSerializer


class WorkshopView(APIView):
    def get(self, request):
        workshops = Workshop.objects.all()
        serializer = WorkshopListSerializer(workshops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = WorkshopCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(host=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkshopDetailView(APIView):
    def get(self, request, workshop_id):
        workshop = get_object_or_404(Workshop, id=workshop_id)
        serializer = WorkshopSerializer(workshop)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, workshop_id):
        workshop = get_object_or_404(Workshop, id=workshop_id)
        if request.user == workshop.host: 
            serializer = WorkshopCreateSerializer(workshop, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, workshop_id):
        workshop = get_object_or_404(Workshop, id=workshop_id)
        if request.user == workshop.host: 
            workshop.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class ApplyView(APIView):
    def post(self, request, workshop_id): # 워크샵 신청
        workshop = get_object_or_404(Workshop, id=workshop_id)
        if request.user != workshop.host: 
            if request.user in workshop.participant.all():
                workshop.participant.remove(request.user)
                return Response({"msg":"워크샵 신청을 취소했습니다."}, status=status.HTTP_200_OK)
            else: 
                WorkshopApply.objects.create(guest=request.user, workshop=workshop, result='대기')       
                return Response({"msg":"워크샵 신청을 접수했습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"해당 workshop의 host는 참가신청할 수 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, workshop_id): # 워크샵 신청 결과 처리
        workshop = get_object_or_404(Workshop, id=workshop_id)
        if request.user == workshop.host: 
            guest = request.data['guest'] # 특정 신청자
            result = request.data['result'] # 신청결과
            workshop_apply = WorkshopApply.objects.get(guest=guest, workshop=workshop)
            workshop_apply.result = f'{result}'
            workshop_apply.save()
            return Response({"msg":f"워크샵 신청을 {result}했습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    def post(self, request, workshop_id):
        workshop = get_object_or_404(Workshop, id=workshop_id)

        if request.user in workshop.likes.all():
            workshop.likes.remove(request.user)
            return Response({"msg":"워크샵 좋아요를 취소했습니다."}, status=status.HTTP_200_OK)
        else: 
            workshop.likes.add(request.user)
            return Response({"msg":"워크샵을 좋아요했습니다."}, status=status.HTTP_200_OK)