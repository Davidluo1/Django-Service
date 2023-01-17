from django.urls import path
from service.views import (AddChefView, AddPetTrainer, AddBarberView, AddDriverView, AddBabySitterView)

urlpatterns = [
    path('chef', AddChefView.as_view()),
    path('pettrainer', AddPetTrainer.as_view()),
    path('barber', AddBarberView.as_view()),
    path('driver', AddDriverView.as_view()),
    path('babysitter', AddBabySitterView.as_view()),
]
