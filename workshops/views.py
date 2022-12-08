from rest_framework.generics import get_object_or_404 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from workshops.models import Workshop, Review, WorkshopApply, Hobby
from workshops.serializers import ReviewSerializer,ReviewCreateSerializer, WorkshopSerializer, WorkshopListSerializer, WorkshopCreateSerializer, HobbySerializer
from rest_framework import permissions


class ReviewView(APIView): # 리뷰 보기/작성
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


class ReviewDetailView(APIView): # 리뷰 수정/삭제
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
            return Response({"msg":"해당 리뷰가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class WorkshopView(APIView):
    def get(self, request):
        category_id = self.request.GET.get('category')
        if category_id:
            workshops = Workshop.objects.filter(category=category_id)
        else:
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


class HobbyView(APIView): # 취미 카테고리
    def get(self, request):
        workshops = Hobby.objects.all()
        serializer = HobbySerializer(workshops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)