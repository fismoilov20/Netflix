from django.shortcuts import render
from django.contrib.postgres.search import TrigramSimilarity

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import filters

from .models import *
from .serializers import *

## Create your views here.

# class MoviesAPIView(APIView):
#     def get(self, request):
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"success": "True", "created_data": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response({"success": "False", "details": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name',]
    ordering_fields = ['rating',]

    def get_queryset(self):
        search = self.request.query_params.get('q')
        if search is not None:
            self.queryset = Movie.objects.annotate(sim=TrigramSimilarity('name',search)).filter(sim__gt=0.35)
            return self.queryset
        return self.queryset

    @action(methods=['GET'], detail=True)
    def comments(self, request, pk):                        ## must take 'pk', not any other name!!!
        comments = Comment.objects.filter(movie__id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

# class ActorsAPIView(APIView):
#     def get(self, request):
#         serializer = ActorSerializer(Actor.objects.all(), many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = ActorSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"success": "True", "created_data": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response({"success": "False", "details": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


# class ActorAPIView(APIView):
#     def put(self, request, pk):
#         serializer = ActorSerializer(Actor.objects.get(id=pk), data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"success": "True", "updated_data": serializer.data})
#         return Response({"success": "False", "details": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

#     def delete(self, request, pk):
#         Actor.objects.get(id=pk).delete()
#         return Response({"message": "Deleted successfuly!"})

class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name',]
    ordering_fields = ['birth_year',]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]

    def create(self, request, *args, **kwargs):                # changing POST request
        serializer = CommentSerializer(data=request.data)      # or  = self.serializer_class(data=request.data) 
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"created_data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error_message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)