from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Session, Review


def is_client(user):
    return user.is_authenticated and user.groups.filter(name='Client').exists()


def is_worker(user):
    return user.is_authenticated and user.groups.filter(name='worker').exists()


def movie_list(request):
    movies = Movie.objects.all()

    title = request.GET.get('title', '')
    genre = request.GET.get('genre', '')
    release_year = request.GET.get('release_year', '')

    if title:
        movies = movies.filter(title__icontains=title)

    if genre:
        movies = movies.filter(genre__icontains=genre)

    if release_year:
        movies = movies.filter(release_year=release_year)

    return render(request, 'movie_list.html', {
        'movies': movies,
        'is_client': is_client(request.user),
        'is_worker': is_worker(request.user),
        'title': title,
        'genre': genre,
        'release_year': release_year,
    })


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST' and is_client(request.user):
        text = request.POST.get('text')
        rating = request.POST.get('rating')

        if text and rating:
            already_reviewed = movie.reviews.filter(user_name=request.user.username).exists()
            if not already_reviewed:
                Review.objects.create(
                    movie=movie,
                    user_name=request.user.username,
                    text=text,
                    rating=rating
                )
                return redirect('movie_detail', movie_id=movie.id)

    sessions = movie.sessions.all().order_by('date_time')
    reviews = movie.reviews.all().order_by('-created_at')
    user_review = None

    if request.user.is_authenticated:
        user_review = movie.reviews.filter(user_name=request.user.username).first()

    return render(request, 'movie_detail.html', {
        'movie': movie,
        'sessions': sessions,
        'reviews': reviews,
        'user_review': user_review,
        'is_client': is_client(request.user),
        'is_worker': is_worker(request.user),
    })


def movie_create(request):
    if not is_worker(request.user):
        return redirect('movie_list')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        release_year = request.POST.get('release_year')
        duration = request.POST.get('duration')
        genre = request.POST.get('genre')
        poster = request.FILES.get('poster')

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
    if not is_worker(request.user):
        return redirect('movie_list')

    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.release_year = request.POST.get('release_year')
        movie.duration = request.POST.get('duration')
        movie.genre = request.POST.get('genre')

        new_poster = request.FILES.get('poster')
        if new_poster:
            movie.poster = new_poster

        movie.save()
        return redirect('movie_detail', movie_id=movie.id)

    return render(request, 'movie_form.html', {'movie': movie})


def movie_delete(request, movie_id):
    if not is_worker(request.user):
        return redirect('movie_list')

    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')

    return render(request, 'movie_confirm_delete.html', {'movie': movie})


def session_list(request):
    sessions = Session.objects.select_related('movie').order_by('date_time')
    return render(request, 'session_list.html', {
        'sessions': sessions,
        'is_worker': is_worker(request.user),
    })


@login_required
def session_create(request):
    if not is_worker(request.user):
        return redirect('session_list')

    movies = Movie.objects.all()

    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        date_time = request.POST.get('date_time')
        hall_number = request.POST.get('hall_number')

        if movie_id and date_time and hall_number:
            movie = get_object_or_404(Movie, id=movie_id)
            Session.objects.create(
                movie=movie,
                date_time=date_time,
                hall_number=hall_number
            )
            return redirect('session_list')

    return render(request, 'session_form.html', {'movies': movies})


@login_required
def session_update(request, session_id):
    if not is_worker(request.user):
        return redirect('session_list')

    session = get_object_or_404(Session, id=session_id)
    movies = Movie.objects.all()

    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        session.date_time = request.POST.get('date_time')
        session.hall_number = request.POST.get('hall_number')

        if movie_id:
            session.movie = get_object_or_404(Movie, id=movie_id)

        session.save()
        return redirect('session_list')

    return render(request, 'session_form.html', {
        'session': session,
        'movies': movies,
    })


@login_required
def session_delete(request, session_id):
    if not is_worker(request.user):
        return redirect('session_list')

    session = get_object_or_404(Session, id=session_id)

    if request.method == 'POST':
        session.delete()
        return redirect('session_list')

    return render(request, 'session_confirm_delete.html', {'session': session})


@login_required
def review_update(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if not is_client(request.user):
        return redirect('movie_detail', movie_id=review.movie.id)

    if review.user_name != request.user.username:
        return redirect('movie_detail', movie_id=review.movie.id)

    if request.method == 'POST':
        review.text = request.POST.get('text')
        review.rating = request.POST.get('rating')
        review.save()
        return redirect('movie_detail', movie_id=review.movie.id)

    return render(request, 'review_form.html', {'review': review})


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    movie_id = review.movie.id

    can_delete = False

    if is_worker(request.user):
        can_delete = True
    elif is_client(request.user) and review.user_name == request.user.username:
        can_delete = True

    if not can_delete:
        return redirect('movie_detail', movie_id=movie_id)

    if request.method == 'POST':
        review.delete()
        return redirect('movie_detail', movie_id=movie_id)

    return render(request, 'review_confirm_delete.html', {'review': review})


@login_required
def profile_view(request):
    my_reviews = Review.objects.filter(user_name=request.user.username).order_by('-created_at')

    return render(request, 'profile.html', {
        'my_reviews': my_reviews,
        'is_client': is_client(request.user),
        'is_worker': is_worker(request.user),
    })