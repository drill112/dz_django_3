from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('sessions/', views.session_list, name='session_list'),
    path('movie/add/', views.movie_create, name='movie_create'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/edit/', views.movie_update, name='movie_update'),
    path('movie/<int:movie_id>/delete/', views.movie_delete, name='movie_delete'),
]