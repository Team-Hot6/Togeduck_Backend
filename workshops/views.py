from rest_framework.generics import get_object_or_404 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from workshops.models import Workshop,Review
from workshops.serializers import ReviewSerializer,ReviewCreateSerializer,WorkshopSerializer
from rest_framework import permissions




class WorkshopView(APIView):
    def get(self, request):
        Workshops = Workshop.objects.all()
        serializer = WorkshopSerializer(Workshops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




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
