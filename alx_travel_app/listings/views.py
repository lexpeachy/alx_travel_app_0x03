from rest_framework import viewsets, permissions, status
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer
import requests
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from .tasks import send_booking_confirmation_email

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]  # for now, open API

    def perform_create(self, serializer):
        # Automatically set owner to the request user if authenticated
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            serializer.save()


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user if self.request.user.is_authenticated else None)

        # Trigger async email task
        send_booking_confirmation_email.delay(
            booking.user.email,
            booking.id,
            booking.listing.title,
            booking.start_date,
            booking.end_date,
            booking.total_price
        )

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=True, methods=["post"])
    def initiate(self, request, pk=None):
        """Initiate a payment with Chapa for a booking"""
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create Payment record
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            status="pending"
        )

        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        data = {
            "amount": str(booking.total_price),
            "currency": "ETB",  # or USD depending on config
            "email": booking.user.email,
            "first_name": booking.user.username,
            "tx_ref": f"tx-{booking.id}-{payment.id}",
            "callback_url": "http://127.0.0.1:8000/api/payments/verify/",  # adjust for prod
            "return_url": "http://127.0.0.1:8000/payment-success/",  # front-end success page
        }

        response = requests.post(
            f"{settings.CHAPA_BASE_URL}/transaction/initialize",
            json=data,
            headers=headers
        )

        if response.status_code == 200:
            resp_data = response.json()
            checkout_url = resp_data.get("data", {}).get("checkout_url")
            payment.transaction_id = data["tx_ref"]
            payment.save()
            return Response({"checkout_url": checkout_url}, status=status.HTTP_200_OK)

        return Response({"error": "Failed to initiate payment"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def verify(self, request):
        """Verify a payment with Chapa"""
        tx_ref = request.data.get("tx_ref")
        if not tx_ref:
            return Response({"error": "Transaction reference required"}, status=status.HTTP_400_BAD_REQUEST)

        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        response = requests.get(
            f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}",
            headers=headers
        )

        if response.status_code == 200:
            resp_data = response.json()
            status_str = resp_data.get("data", {}).get("status")

            try:
                payment = Payment.objects.get(transaction_id=tx_ref)
                if status_str == "success":
                    payment.status = "completed"
                    payment.save()
                    return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
                else:
                    payment.status = "failed"
                    payment.save()
                    return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)
            except Payment.DoesNotExist:
                return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)
