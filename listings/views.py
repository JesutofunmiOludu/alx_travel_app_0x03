from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Listing, Review, Booking , Payment
from .serializers import ListingSerializer, ReviewSerializer, BookingSerializer ,PaymentSerializer
from rest_framework import viewsets, views
from rest_framework.views import APIView
import uuid
import requests
from django.conf import settings


# Create your views here.


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
"""
@api_view(['GET'])
def listing_list(request):
    listings = Listing.objects.all()
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def listing_detail(request, pk):
    try:
        listing = Listing.objects.get(property_id=pk)
    except Listing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ListingSerializer(listing)
    return Response(serializer.data)
@api_view(['POST'])
def listing_create(request):
    serializer = ListingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def listing_update(request, pk):
        try:
        listing = Listing.objects.get(property_id=pk)
    except Listing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ListingSerializer(listing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def listing_delete(request, pk):
    try:
        listing = Listing.objects.get(property_id=pk)
    except Listing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    listing.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    """

class InitiateChapaPayment(APIView):
    """
    Initiate a payment with Chapa and return the payment URL or data to client.
    """

    def post(self, request):
        # expected json: { "booking_reference": "BK123", "amount": 100, "email": "customer@example.com", "first_name": "John", "last_name": "Doe" }
        data = request.data
        booking_ref = data.get("booking_reference")
        amount = data.get("amount")
        email = data.get("email")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")

        if not booking_ref or not amount or not email:
            return Response({"detail": "booking_reference, amount and email required"}, status=status.HTTP_400_BAD_REQUEST)

        # create tx_ref: unique reference for merchant (use booking_ref + uuid)
        tx_ref = f"{booking_ref}-{uuid.uuid4().hex[:8]}"

        # create Payment record in our DB with status Pending
        payment = Payment.objects.create(
            booking_reference=booking_ref,
            amount=amount,
            currency="ETB",
            status=Payment.STATUS_PENDING,
            chapa_tx_ref=tx_ref
        )

        # prepare payload for Chapa initialize endpoint
        chapa_url = f"{settings.CHAPA_BASE_URL.rstrip('/')}/transaction/initialize"
        payload = {
            "amount": str(amount),  # Chapa expects numeric, but some sdks accept string
            "currency": "ETB",
            "tx_ref": tx_ref,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            # optional
            "callback_url": request.build_absolute_uri("/api/listings/chapa/callback/"),
            "return_url": request.build_absolute_uri("/payment/success/"),
            "description": f"Payment for booking {booking_ref}"
        }

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        try:
            resp = requests.post(chapa_url, json=payload, headers=headers, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            # update payment as failed and return error
            payment.status = Payment.STATUS_FAILED
            payment.metadata = {"error": str(e)}
            payment.save()
            return Response({"detail": "error initialising payment", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        chapa_resp = resp.json()
        # typical chapa initialize response contains data and checkout_url
        data = chapa_resp.get("data", {})
        checkout_url = data.get("checkout_url") or data.get("authorization_url") or data.get("payment_url")

        # store chapa transaction id if present (many responses include 'id' or 'transaction_id')
        chapa_tx_id = data.get("id") or data.get("transaction_id")
        if chapa_tx_id:
            payment.chapa_tx_id = chapa_tx_id
        payment.metadata = chapa_resp
        payment.save()

        return Response({
            "payment_id": payment.id,
            "tx_ref": tx_ref,
            "checkout_url": checkout_url,
            "chapa_response": chapa_resp
        }, status=status.HTTP_200_OK)


class VerifyChapaPayment(APIView):
    """
    Verify a Chapa transaction using tx_ref or transaction id.
    """

    def post(self, request):
        # expected: { "tx_ref": "..." } or { "chapa_tx_id": "..." }
        tx_ref = request.data.get("tx_ref")
        chapa_tx_id = request.data.get("chapa_tx_id")

        if tx_ref:
            url = f"{settings.CHAPA_BASE_URL.rstrip('/')}/transaction/verify/{tx_ref}"
            # Note: some Chapa docs use /transaction/verify?tx_ref= or path-based; check your docs.
        elif chapa_tx_id:
            url = f"{settings.CHAPA_BASE_URL.rstrip('/')}/transaction/verify/{chapa_tx_id}"
        else:
            return Response({"detail": "tx_ref or chapa_tx_id required"}, status=status.HTTP_400_BAD_REQUEST)

        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            return Response({"detail": "error verifying payment", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        chapa_resp = resp.json()
        # typical success: chapa_resp['status'] or chapa_resp['data']['status'] etc.
        # Normalize reading:
        data = chapa_resp.get("data") or {}
        payment_status = data.get("status") or chapa_resp.get("status") or None
        tx_ref_resp = data.get("tx_ref") or data.get("reference") or None

        # find our Payment
        payment = None
        if tx_ref:
            try:
                payment = Payment.objects.get(chapa_tx_ref=tx_ref)
            except Payment.DoesNotExist:
                payment = None
        elif chapa_tx_id:
            try:
                payment = Payment.objects.get(chapa_tx_id=chapa_tx_id)
            except Payment.DoesNotExist:
                payment = None

        # update payment record based on status
        if payment:
            if payment_status and payment_status.lower() == "success":
                payment.status = Payment.STATUS_COMPLETED
            else:
                # some status values may be 'failed' or 'cancelled'
                if payment_status and payment_status.lower() in ("failed","cancelled"):
                    payment.status = Payment.STATUS_FAILED
                else:
                    # if uncertain, keep pending but record response
                    payment.status = payment.status or Payment.STATUS_PENDING
            payment.metadata = chapa_resp
            payment.save()

        return Response({"chapa_response": chapa_resp, "updated_payment": PaymentSerializer(payment).data if payment else None})

class ChapaCallback(APIView):
    """
    Handle Chapa callback (redirect)
    """
    def get(self, request):
        tx_ref = request.GET.get("tx_ref")
        status_param = request.GET.get("status")
        return Response({
            "tx_ref": tx_ref, 
            "status": status_param, 
            "message": "Payment callback received. Please return to the app to verify status."
        }, status=status.HTTP_200_OK)