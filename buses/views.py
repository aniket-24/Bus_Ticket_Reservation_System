from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bus
from .serializers import BusSerializer
from django.utils.timezone import datetime

class BusSearchView(APIView):
    """
    API endpoint for searching buses based on source, destination, and date.
    """
    def get(self, request):
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')
        date = request.query_params.get('date')  # Format: YYYY-MM-DD

        if not date:
            return Response({"error": "Date is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')

            buses = Bus.objects.filter(
                source=source,
                destination=destination,
                frequency__icontains=day_of_week
            )

            serializer = BusSerializer(buses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
