from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, ReviewViewSet, InitiateChapaPayment, VerifyChapaPayment, ChapaCallback

router = DefaultRouter()
# example: register a viewset later
# router.register(r'properties', views.PropertyViewSet)
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("chapa/initiate/", InitiateChapaPayment.as_view(), name="chapa-initiate"),
    path("chapa/verify/", VerifyChapaPayment.as_view(), name="chapa-verify"),
    path("chapa/callback/", ChapaCallback.as_view(), name="chapa-callback"),
]