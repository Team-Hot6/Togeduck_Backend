from rest_framework.generics import get_object_or_404 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from workshops.models import Workshop, Review, WorkshopApply, Hobby, Location
from workshops.serializers import ReviewSerializer,ReviewCreateSerializer, WorkshopSerializer, WorkshopListSerializer, WorkshopCreateSerializer, HobbySerializer, LocationSerializer, WorkshopApplySerializer
from rest_framework import permissions
from workshops.paginations import workshop_page
from rest_framework.generics import ListAPIView
from django.db.models import Count, Q
import json, os
from pathlib import Path


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


class WorkshopView(ListAPIView):
    pagination_class = workshop_page
    serializer_class = WorkshopListSerializer
    queryset = Workshop.objects.all().order_by('-created_at')
    
    def get(self, request):
        category_id = self.request.GET.get('category')

        sort = self.request.GET.get('sort')

        # sort와 category string이 둘 다 있을때
        if sort and category_id:
            if sort == 'like':
                self.queryset = Workshop.objects.filter(category=category_id).annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
            elif sort == 'latest':
                self.queryset = Workshop.objects.filter(category=category_id).order_by('-created_at')
        
        # category id 값만 있을때
        if category_id and not sort:
            self.queryset = Workshop.objects.filter(category=category_id).order_by('-created_at')    
        
        # sort 값만 있을때
        if sort and not category_id:
            if sort == 'like':
                self.queryset = Workshop.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
            elif sort == 'latest':
                self.queryset = Workshop.objects.all().order_by('-created_at')

        pages = self.paginate_queryset(self.get_queryset())
        slz = self.get_serializer(pages, many=True)

        return self.get_paginated_response(slz.data)
    
    def post(self, request):
      
        serializer = WorkshopCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(host=request.user)
            print('adsadasdasdsadsadsadsad')
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# workshop lanking 순으로 정렬된 파일 읽어서 리턴
class WorkshopLankView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        BASE_DIR = Path(__file__).resolve().parent.parent
        lank_file_path = os.path.join(BASE_DIR, 'Lank.json')
        
        with open(lank_file_path, "r") as f:
            result_lanking = json.load(f)
        lank_list = result_lanking['result_workshop_lank']

        query_list = []

        for idx in lank_list:
            try:
                obj = Workshop.objects.get(id=idx)
                query_list.append(obj)
            except:
                continue
        
        if not query_list:
            obj = Workshop.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')[0:7]
            slz = WorkshopListSerializer(obj, many=True)
            return Response(slz.data, status=status.HTTP_200_OK)
            
        slz = WorkshopListSerializer(query_list, many=True)

        return Response(slz.data, status=status.HTTP_200_OK)


class WorkshopDetailView(APIView):
    def get(self, request, workshop_id):
        workshop = get_object_or_404(Workshop, id=workshop_id)
        workshop.views += 1
        workshop.save()
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
    def get(self, request, workshop_id): # 워크샵 신청 관리 페이지 조회 (승인/거절)
        workshop = get_object_or_404(Workshop, id=workshop_id)
        if request.user == workshop.host:
            workshop_apply = WorkshopApply.objects.filter(workshop=workshop_id)
            if not workshop_apply:
                serializer = WorkshopSerializer(workshop)
            else:
                serializer = WorkshopApplySerializer(workshop_apply, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

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
        hobbys = Hobby.objects.all()
        serializer = HobbySerializer(hobbys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocationView(APIView): # 지역 카테고리
    def get(self, request):
        Locations = Location.objects.all()
        serializer = LocationSerializer(Locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkshopPopularView(APIView):
    def get(self, request):
        popular_workshop = Workshop.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')[:7]
        serializer = WorkshopListSerializer(popular_workshop, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)