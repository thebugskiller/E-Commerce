import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from cart.views import CartViewSet
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateChargeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Stripe card token'),
                },
                required=['token']
            ),
            responses={200: 'Payment successful'}
        )
    def post(self, request):
        try:
            # Get the card token from the request body
            token = request.data.get('token')
            if not token:
                return Response({'error': 'No card token provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Get the total price from the user's cart
            cart_viewset = CartViewSet()
            cart_viewset.request = request
            total_price_response = cart_viewset.total_price(request)
            total_amount = total_price_response.data['total_price']

            # Convert total_amount to cents (Stripe expects amounts in cents)
            amount_in_cents = int(total_amount * 100)

            # Create a charge using Stripe
            charge = stripe.Charge.create(
                amount=amount_in_cents,
                currency='usd',
                source=token,
                description=f'Charge for {request.user.username}'
            )

            return Response({
                'message': 'Payment successful',
                'amount': total_amount,
                'charge_id': charge.get('id')
            })
        except stripe.error.CardError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
