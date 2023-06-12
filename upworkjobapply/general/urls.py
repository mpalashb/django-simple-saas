from django.urls import path
from general.views import (
    home,
    PlanList,
    PlanDetail,
    PaymentSuccess,
    PaymentCancel,
    TestPayNow,
    HandleSubCancel,
    stripe_webhook
)

app_name = "general"

urlpatterns = [
    path('', home, name='gen-index'),
    path('cancel-sub', HandleSubCancel.as_view(), name='cancel-sub'),
    path('stripe-webhook', stripe_webhook, name='stripe-webhook'),
    path('plan-checkout-session/<int:pk>', TestPayNow.as_view(),
         name='plan-checkout-session'),
    path('payment-success', PaymentSuccess.as_view(), name='payment-success'),
    path('payment-cancel', PaymentCancel.as_view(), name='payment-cancel'),
    path('plan-list', PlanList.as_view(), name='plan-list'),
    path('plan/<int:pk>', PlanDetail.as_view(), name='plan-detail'),
]
