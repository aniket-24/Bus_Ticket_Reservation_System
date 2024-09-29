from django.urls import path
from .views import BusSearchView

urlpatterns = [
    path('search/', BusSearchView.as_view(), name='bus-search'),
]
