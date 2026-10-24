from django.shortcuts import render
from rest_framework import viewsets
from .models import Price
from .serializers import PriceSerializer
# Create your views here.

class PriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    look_up_field = 'code'