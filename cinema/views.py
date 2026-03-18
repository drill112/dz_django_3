from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Session, Review


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        text = request.POST.get('text')
        rating = request.POST.get('rating')

        if user_name and text and rating:
            Review.objects.create(
                movie=movie,
                user_name=user_name,
                text=text,
                rating=rating
            )
            return redirect('movie_detail', movie_id=movie.id)

    sessions = movie.sessions.all().order_by('date_time')
    reviews = movie.reviews.all().order_by('-created_at')

    return render(request, 'movie_detail.html', {
        'movie': movie,
        'sessions': sessions,
        'reviews': reviews
    })


def movie_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        release_year = request.POST.get('release_year')
        duration = request.POST.get('duration')
        genre = request.POST.get('genre')
        poster = request.POST.get('poster')

        if title and description and release_year and duration and genre and poster:
            Movie.objects.create(
                title=title,
                description=description,
                release_year=release_year,
                duration=duration,
                genre=genre,
                poster=poster
            )
            return redirect('movie_list')

    return render(request, 'movie_form.html')


def movie_update(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.release_year = request.POST.get('release_year')
        movie.duration = request.POST.get('duration')
        movie.genre = request.POST.get('genre')
        movie.poster = request.POST.get('poster')
        movie.save()
        return redirect('movie_detail', movie_id=movie.id)

    return render(request, 'movie_form.html', {'movie': movie})


def movie_delete(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')

    return render(request, 'movie_confirm_delete.html', {'movie': movie})


def session_list(request):
    sessions = Session.objects.select_related('movie').order_by('date_time')
    return render(request, 'session_list.html', {'sessions': sessions})