from django.contrib import admin
from .models import Movie, Session, Review, TicketBooking, FavoriteMovie

admin.site.register(Movie)
admin.site.register(Session)
admin.site.register(Review)
admin.site.register(TicketBooking)
admin.site.register(FavoriteMovie)