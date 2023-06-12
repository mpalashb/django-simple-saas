from django.utils import timezone
from users.models import Profile
from django.contrib.auth.models import User
from general.models import Subscription
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse, HttpResponse
import stripe
import json
from django.conf import settings
from django.views.generic import (
    DetailView, ListView, CreateView, TemplateView
)

from django.views import View
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from general.models import (
    Plan
)

stripe.api_key = settings.STRIPE_SECRECT_KEY


def home(request):
    return render(request, 'general_app/index.html')


class PaymentSuccess(TemplateView):
    template_name = 'common/payment-success.html'


class PaymentCancel(TemplateView):
    template_name = 'common/payment-cancel.html'


@csrf_exempt
def stripe_webhook(request):
    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_KEY
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata')

        print('Session========================================')
        print(session)
        print('Session========================================')
        print('\n')
        print('Metadata========================================')
        print(metadata)
        print('Metadata========================================')

        Subscription.objects.get_or_create(
            customer_id=session['customer'],
            sub_id=session['subscription'],
            user=Profile.objects.get(id=int(metadata['profile_id'])),
            plan=Plan.objects.get(id=int(metadata['product_id'])),
            active=True,
            start=timezone.now(),

        )

    return HttpResponse(status=200)


class HandleSubCancel(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        sub_get = Subscription.objects.filter(
            user=request.user.profile.id).last()
        # print(sub_get.sub_id)

        stripe.Subscription.delete(
            sub_get.sub_id
        )

        return redirect('users:profile-dash')


class TestPayNow(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):

        domain = "http://127.0.0.1:8000"
        pk_kwargs = kwargs.get('pk')
        plan_obj = get_object_or_404(Plan, pk=pk_kwargs)

        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.profile.email,
            payment_method_types=['card'],
            line_items=[
                # {
                #     "price_data": {
                #         "currency": "usd",
                #         "product_data": {
                #             "name": plan_obj.name
                #         },
                #         "unit_amount": 100*int(plan_obj.plan_cost),
                #     },
                #     "quantity": 1,
                # }
                # {"price": "price_1N0kwOGak6VGK7rT2mQiw3w4", "quantity": 1}
                {"price": plan_obj.stripe_product_id, "quantity": 1}
            ],
            metadata={
                "product_id": plan_obj.id,
                "user": request.user,
                "profile_id": request.user.profile.id
            },
            mode='subscription',
            # mode='payment',
            success_url=f'{domain}/payment-success',
            cancel_url=f'{domain}/payment-cancel',

        )

        return JsonResponse({'id': checkout_session.id})


class PlanList(ListView):
    model = Plan
    template_name = 'common/plan-list.html'
    context_object_name = 'plans'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan_monthly = self.get_queryset().filter(plan_type='monthly').all()
        plan_yearly = self.get_queryset().filter(plan_type='yearly').all()
        print(plan_yearly)
        for p in plan_monthly:
            print(p.plan_feat_list)

        context['plan_monthly'] = plan_monthly
        context['plan_yearly'] = plan_yearly
        return context


class PlanDetail(LoginRequiredMixin, DetailView):
    model = Plan
    template_name = 'common/plan-detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super(PlanDetail, self).get_context_data(**kwargs)
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        context['plan_features'] = json.loads(self.get_queryset().filter(
            id=self.kwargs.get('pk')).first().plan_features)

        return context

    def get_object(self, queryset=None):
        plans_obj = self.get_queryset().filter(
            pk=self.kwargs.get(self.pk_url_kwarg)).first()
        return plans_obj
