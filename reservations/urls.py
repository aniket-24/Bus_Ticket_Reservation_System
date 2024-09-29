from django.urls import path
from .views import CreateReservationView, UserReservationsView

urlpatterns = [
    path('reserve/', CreateReservationView.as_view(), name='create-reservation'),
    path('user/<int:user_id>/', UserReservationsView.as_view(), name='user_reservations'),
]
