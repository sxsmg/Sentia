from django.urls import path
from api import views

urlpatterns = [
    path('api/register/', views.register_user, name='register_user'),
    path('api/login/', views.login_user, name='login_user'),
    path('api/exercises/', views.get_exercises, name='get_exercises'),
    path('api/exercises/<int:exercise_id>/submit/', views.submit_response, name='submit_response'),
]