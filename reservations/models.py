from django.db import models
from buses.models import Bus

class Reservation(models.Model):
    user_id = models.IntegerField()  # According to problem statement => Simple User Identification, not authentication
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    reserved_seats = models.IntegerField()
    reservation_date = models.DateField()

    def __str__(self):
        return f'Reservation for User {self.user_id} on {self.bus.bus_number}'
