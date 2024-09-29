from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .serializers import ReservationSerializer
from buses.models import Bus
from django.db.models import Sum
from datetime import datetime

class CreateReservationView(APIView):
    """
    API endpoint for creating a reservation for a bus.
    """
    def post(self, request):
        user_id = request.data.get('user_id')
        bus_id = request.data.get('bus')
        reserved_seats = request.data.get('reserved_seats')
        reservation_date_str = request.data.get('reservation_date')

        try:
            reservation_date = datetime.strptime(reservation_date_str, "%Y-%m-%d").date()
            # Calculating the day of the week
            reservation_day = reservation_date.strftime("%A") 

            bus = Bus.objects.get(id=bus_id)

            active_days = bus.frequency.split(',')
            if reservation_day not in active_days:
                return Response({"error": f"Bus is not active on {reservation_day}"}, status=status.HTTP_400_BAD_REQUEST)

            total_reserved_seats = Reservation.objects.filter(bus=bus, reservation_date=reservation_date).aggregate(Sum('reserved_seats'))['reserved_seats__sum'] or 0
            available_seats = bus.total_seats - total_reserved_seats

            if reserved_seats > available_seats:
                return Response({"error": "Not enough seats available"}, status=status.HTTP_400_BAD_REQUEST)

            reservation_data = {
                "user_id": user_id,
                "bus": bus.id,
                "reserved_seats": reserved_seats,
                "reservation_date": reservation_date 
            }

            serializer = ReservationSerializer(data=reservation_data)
            if serializer.is_valid():
                reservation = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Bus.DoesNotExist:
            return Response({"error": "Bus not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserReservationsView(APIView):
    """
    API endpoint for retrieving all reservations made by a specific user.
    """
    def get(self, request, user_id):
        try:
            reservations = Reservation.objects.filter(user_id=user_id)

            serializer = ReservationSerializer(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
