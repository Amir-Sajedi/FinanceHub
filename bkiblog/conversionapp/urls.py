from django.urls import path
from .views import ConversionViewView

urlpatterns = [
    path('', ConversionViewView.as_view(), name='converter'),
]
