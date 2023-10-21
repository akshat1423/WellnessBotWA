from django.urls import path
from . import views  # Import views
from .views import bot

urlpatterns = [
    path("bot/", bot),  # Added a comma here
    path('queries_over_time/', views.queries_over_time, name='queries_over_time'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
