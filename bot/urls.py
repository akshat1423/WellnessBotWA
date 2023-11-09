from django.urls import path
from .views import bot
from . views import dashboard
from .views import queries_over_time
urlpatterns = [
    path("bot/", bot),  # Added a comma here
    path('queries_over_time/', queries_over_time, name='queries_over_time'),
    path('dashboard/', dashboard, name='dashboard'),
]
