from django.urls import path
from .views import ConversionViewView, NetWorthView

urlpatterns = [
    path('', ConversionViewView.as_view(), name='converter'),
    path('networth/', NetWorthView.as_view(), name='networth'),
]
