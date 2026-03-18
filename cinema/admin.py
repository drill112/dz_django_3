from django.contrib import admin
from .models import Movie, Session, Review

admin.site.register(Movie)
admin.site.register(Session)
admin.site.register(Review)