from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from materials.serializers import PaymentSerializer
from users.models import Subscription, Payment
from users.services import convert_rub_to_dollars, create_start_price, create_stripe_sessions


class SubscriptionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        sub_item = Subscription.objects.filter(user=user, course=course)

        if sub_item.exists():
            sub_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'

        return Response({"message": message})

    class PaymentCreateAPIView(CreateAPIView):
        serializer_class = PaymentSerializer
        queryset = Payment.objects.all()

        def perform_create(self, serializer):
            payment = serializer.save(user=self.request.user)
            amount_in_dollars = convert_rub_to_dollars(payment.amount)
            price = create_start_price(amount_in_dollars)
            session_id, payment_link = create_stripe_sessions(price)
            payment.session_id = session_id
            payment.link = payment_link
            payment.save()
