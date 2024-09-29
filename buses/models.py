from django.db import models

class Bus(models.Model):
    company_name = models.CharField(max_length=100)
    bus_number = models.CharField(max_length=20, unique=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    frequency = models.CharField(max_length=100)  # frequency = "Monday,Tuesday"
    total_seats = models.IntegerField()

    def __str__(self):
        return f'{self.company_name} - {self.bus_number}'
