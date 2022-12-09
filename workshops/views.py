from rest_framework.generics import get_object_or_404 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from workshops.models import Workshop, WorkshopApply, Review
from workshops.serializers import ReviewSerializer,ReviewCreateSerializer, WorkshopSerializer, WorkshopListSerializer, WorkshopCreateSerializer
from rest_framework import permissions
from workshops.paginations import workshop_page
from rest_framework.generics import ListAPIView


# 댓글 보기/작성
class ReviewView(APIView):
    def get(self, request, workshop_id):
        article = get_object_or_404(Workshop,id=workshop_id) 
        reviews = article.review_workshop.all() 
        serializer = ReviewSerializer(reviews, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, workshop_id):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save(user=request.user, workshop_id=workshop_id) 
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 수정/삭제
class ReviewDetailView(APIView):
    def put(self, request, workshop_id,reviews_id): 
        reviews = get_object_or_404(Review,id=reviews_id) 
        if request.user == reviews.user: 
            serializer = ReviewCreateSerializer(reviews, data=request.data) 
            if serializer.is_valid(): 
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK) 
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, reviews_id, workshop_id):
        reviews = get_object_or_404(Review,id=reviews_id) 
        if request.user == reviews.user:
            reviews.delete()
            return Response("삭제완룔료룔", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한 없다고", status=status.HTTP_403_FORBIDDEN)


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

# pagination 적용
class WorkshopView_2(ListAPIView):
    pagination_class = workshop_page
    serializer_class = WorkshopListSerializer
    queryset = Workshop.objects.all()
    
    def get(self, request):
        pages = self.paginate_queryset(self.get_queryset())
        slz = self.get_serializer(pages, many=True)

        return self.get_paginated_response(slz.data)
    
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
