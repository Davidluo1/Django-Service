from django.urls import path
from user.views import (UserSignUpView, UserLoginView, UserList, NearbyBarber, NearbyChef, NearbyDriver,
                        NearbyBabysitter, NearbyPetTrainer, ChefReservation, DriverReservation, 
                        BarberReservation, PetTrainerReservation, BabySitterReservation)

urlpatterns = [
    path('signup', UserSignUpView.as_view()),
    path('login', UserLoginView.as_view()),
    path('list', UserList.as_view()),
    path('barberlist/<int:user_id>', NearbyBarber.as_view()),
    path('cheflist/<int:user_id>', NearbyChef.as_view()),
    path('driverlist/<int:user_id>', NearbyDriver.as_view()),
    path('babysitterlist/<int:user_id>', NearbyBabysitter.as_view()),
    path('pettrainerlist/<int:user_id>', NearbyPetTrainer.as_view()),
    path('chef/reserve/<int:chef_id>', ChefReservation.as_view()),
    path('driver/reserve/<int:driver_id>', DriverReservation.as_view()),
    path('barber/reserve/<int:barber_id>', BarberReservation.as_view()),
    path('pettrainer/reserve/<int:pettrainer_id>', PetTrainerReservation.as_view()),
    path('babysitter/reserve/<int:babysitter_id>', BabySitterReservation.as_view()),
]
