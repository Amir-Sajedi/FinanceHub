from rest_framework.routers import DefaultRouter
from .views import PriceViewSet


router = DefaultRouter()
router.register('prices', PriceViewSet, basename='price')
urlpatterns = router.urls