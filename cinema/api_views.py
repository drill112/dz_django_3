from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Movie, Session, Review
from .serializers import MovieSerializer, SessionSerializer, ReviewSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CinemaStatsAPIView(APIView):
    def get(self, request):
        average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
        total_users = User.objects.count()
        total_movies = Movie.objects.count()

        return Response({
            'average_rating': average_rating if average_rating else 0,
            'total_users': total_users,
            'total_movies': total_movies,
        })