from rest_framework.generics import get_object_or_404 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from workshops.models import Workshop,Review,Hobby
from workshops.serializers import ReviewSerializer,ReviewCreateSerializer,WorkshopSerializer,WorkshopCreateSerializer,WorkshopListSerializer,HobbySerializer
from rest_framework import permissions
from workshops.paginations import workshop_page
from rest_framework.generics import ListAPIView



class WorkshopView(ListAPIView):
    pagination_class = workshop_page
    serializer_class = WorkshopListSerializer
    queryset = Workshop.objects.all().order_by('-created_at')
    
    def get(self, request):
        category_id = self.request.GET.get('category')

        if category_id:
            self.queryset = Workshop.objects.filter(category=category_id).order_by('-created_at')

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



# 취미 카테고리
class HobbyView(APIView):
    def get(self, request):
        workshops = Hobby.objects.all()
        serializer = HobbySerializer(workshops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    




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
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, workshop_id):
        workshop = get_object_or_404(Workshop, id=workshop_id)
        if request.user == workshop.host: 
            workshop.delete()
            return Response('워크샵 삭제',status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)




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
            return Response("삭제합니다", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한 없다", status=status.HTTP_403_FORBIDDEN)








# 좋아요
class LikeView(APIView):
    def post(self, request, workshop_id):
        workshop = get_object_or_404(Workshop, id=workshop_id)

        if request.user in workshop.likes.all():
            workshop.likes.remove(request.user)
            return Response({"msg":"워크샵 좋아요를 취소했습니다."}, status=status.HTTP_200_OK)
        else: 
            workshop.likes.add(request.user)
            return Response({"msg":"워크샵을 좋아요했습니다."}, status=status.HTTP_200_OK)