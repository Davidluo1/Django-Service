from django.urls import path
from service.views import (AddChefView, AddPetTrainer, AddBarberView, AddDriverView, AddBabySitterView, 
                           UpdateChef, UpdateDriver, UpdateBarber, UpdateBabySitter, UpdatePetTrainer)

urlpatterns = [
    path('chef', AddChefView.as_view()),
    path('pettrainer', AddPetTrainer.as_view()),
    path('barber', AddBarberView.as_view()),
    path('driver', AddDriverView.as_view()),
    path('babysitter', AddBabySitterView.as_view()),
    path('chef/<int:chef_id>', UpdateChef.as_view()),
    path('driver/<int:driver_id>', UpdateDriver.as_view()),
    path('barber/<int:barber_id>', UpdateBarber.as_view()),
    path('babysitter/<int:babysitter_id>', UpdateBabySitter.as_view()),
    path('pettrainer/<int:pettrainer_id>', UpdatePetTrainer.as_view()),
]
