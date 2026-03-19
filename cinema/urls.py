from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('sessions/', views.session_list, name='session_list'),

    path('movie/add/', views.movie_create, name='movie_create'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/edit/', views.movie_update, name='movie_update'),
    path('movie/<int:movie_id>/delete/', views.movie_delete, name='movie_delete'),

    path('session/add/', views.session_create, name='session_create'),
    path('session/<int:session_id>/edit/', views.session_update, name='session_update'),
    path('session/<int:session_id>/delete/', views.session_delete, name='session_delete'),

    path('review/<int:review_id>/edit/', views.review_update, name='review_update'),
    path('review/<int:review_id>/delete/', views.review_delete, name='review_delete'),

    path('profile/', views.profile_view, name='profile'),
]