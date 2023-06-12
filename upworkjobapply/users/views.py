
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import (
    ObjectDoesNotExist
)
from django import http
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.utils import timezone
from django.db import models
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from general.models import Subscription
from users.forms import ProfileForm
from typing import Any, Dict, Optional
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.views.generic import (
    DetailView, ListView, CreateView,
    DeleteView, View, TemplateView,
    FormView,
)
from users.permissions.profile import (
    IsOwnerProfile
)

from general.models import (
    Plan
)

from users.models import (
    Profile, GeneratedProposal, CheckedProposal,
)

from users.forms import (
    GenCoverForm, ModifyUserCreationForm
)
from django.contrib.auth.views import (
    LoginView, LogoutView
)

from django.conf import settings
import stripe
from utils.openai_prompt import (
    gen_proposal,
)


stripe.api_key = settings.STRIPE_SECRECT_KEY


class UserCreateView(CreateView):
    form_class = ModifyUserCreationForm
    template_name = 'user_app/register.html'
    success_url = reverse_lazy('users:login')

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    # def form_invalid(self, form: BaseModelForm) -> HttpResponse:
    #     return self.render_to_response(self.get_context_data(form=form))


class AuthLogoutView(LogoutView):
    pass


class AuthView(LoginView):
    template_name = 'user_app/login.html'
    success_url = reverse_lazy('users:profile-dash')

    # def form_valid(self, form: AuthenticationForm) -> HttpResponse:
    #     super().form_valid(form)
    #     return redirect('users:profile-dash')

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)


class ClearCheckCoverHistory(LoginRequiredMixin, TemplateView):
    model = CheckedProposal

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.model.objects.filter(user=request.user.profile).all().delete()

        return redirect('users:check-proposal-history')


class CheckCoverHistory(LoginRequiredMixin, ListView):
    template_name = 'user_app/check-cover-history.html'
    model = CheckedProposal
    context_object_name = 'history'

    def get_queryset(self) -> QuerySet[Any]:
        try:

            if self.request.user.profile:
                c_query = super().get_queryset()
                c_query = c_query.filter(
                    user=self.request.user.profile).all().order_by('-created_at')

                return c_query
        except ObjectDoesNotExist:

            return None
        except:
            return None


class CheckCoverLeter(LoginRequiredMixin, TemplateView):
    template_name = 'user_app/check-cover.html'


class ClearProposalHistory(LoginRequiredMixin, View):
    model = GeneratedProposal

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.model.objects.filter(user=request.user.profile).all().delete()

        return redirect('users:proposal-history')


class ProposalHistory(LoginRequiredMixin, ListView):
    template_name = 'user_app/gen-cover-history.html'
    model = GeneratedProposal
    context_object_name = 'history'

    def get_queryset(self) -> QuerySet[Any]:
        try:
            if self.request.user.profile:
                c_query = super().get_queryset()
                c_query = c_query.filter(
                    user=self.request.user.profile).all().order_by('-created_at')

                return c_query
        except ObjectDoesNotExist:
            return None
        except:
            return None

        # return self.request.user.profile.proposals.all().order_by('-created_at')


class GenCoverLeter(LoginRequiredMixin, FormView):

    template_name = 'user_app/gen-cover.html'
    form_class = GenCoverForm
    success_url = reverse_lazy('users:gen-cover')

    def form_valid(self, form: Any) -> HttpResponse:
        title = form.cleaned_data['title']
        desc = form.cleaned_data['desc']
        client_name = form.cleaned_data['client']
        type_option = form.cleaned_data['type_option']

        max_len = 2500

        if len(title) > max_len or len(desc) > max_len:
            return HttpResponse(f'Length must be less than {max_len}')

        custom_context = self.get_context_data()

        try:
            credit_left = self.request.user.profile.credit
        except ObjectDoesNotExist:
            credit_left: int = None

        if credit_left and credit_left >= 5:
            try:
                try:
                    profile_ins = Profile.objects.get(user=self.request.user)
                except ObjectDoesNotExist:
                    profile_ins = None

                if profile_ins:
                    res = gen_proposal(
                        title=title,
                        desc=desc,
                        client_name=client_name,
                        type_of=type_option
                    )

                    # print('This response of openai')
                    # print(res)
                    # print('This response of openai')

                    # res = f'Dear, [Client Name], asasasasasasas, asasasasasasasas asas, {title} {desc} {client_name} {type_option}'

                    GeneratedProposal.objects.create(
                        user=self.request.user.profile,
                        cover_leter=f"{res}"
                    )
                    if res:
                        profile_ins.credit -= 5
                        profile_ins.save()
                        custom_context['credit_left'] = profile_ins.credit

            except Exception as p:
                print(p)
                res = None

        else:
            custom_context['credit_error'] = '''Make sure you have a profile and enough credit!'''
            return render(self.request, self.template_name, context=custom_context)

        custom_context['cover_leter'] = f"{res}"

        return render(self.request, self.template_name, context=custom_context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user_app/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['has_profile'] = True
        if not Profile.objects.filter(user=self.request.user).first():
            context['has_profile'] = False
            return context

        cus_sub = Subscription.objects.filter(
            user=self.request.user.profile).last()

        if cus_sub:
            print('\n')
            print(f'{cus_sub.customer_id}')
            print('\n')

            retrive_subs = stripe.Subscription.retrieve(
                cus_sub.sub_id
            )

            # "sub_1NEstPGak6VGK7rTkoaqyHid"

            status = retrive_subs['status']
            canceled_at = retrive_subs['canceled_at']
            plan_interval = retrive_subs['plan']['interval']

            current_period_start_timestamp = retrive_subs['current_period_start']
            current_period_end_timestamp = retrive_subs['current_period_end']

            date_start = None
            date_end = None
            canceled_date = None

            if current_period_start_timestamp:
                date_start = timezone.datetime.fromtimestamp(
                    int(current_period_start_timestamp)).strftime('%Y-%m-%d %H:%M')

            if current_period_end_timestamp:
                date_end = timezone.datetime.fromtimestamp(
                    int(current_period_end_timestamp)).strftime('%Y-%m-%d %H:%M')

            if canceled_at:
                canceled_date = timezone.datetime.fromtimestamp(
                    int(canceled_at)).strftime('%Y-%m-%d %H:%M')

            context['date_start'] = date_start
            context['date_end'] = date_end
            context['status'] = status
            context['canceled_date'] = canceled_date
            context['plan_interval'] = plan_interval

        return context

    def get_object(self, queryset=None) -> Profile:
        if not Profile.objects.filter(user=self.request.user).first():
            return None

        return self.request.user.profile


class DelProfile(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        Profile.objects.filter(user=self.request.user).first().delete()
        return redirect("users:profile-dash")


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = "user_app/profile-form.html"
    form_class = ProfileForm

    success_url = reverse_lazy('users:profile-dash')

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if Profile.objects.filter(user=self.request.user).first():
            return redirect('users:profile-dash')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['has_profile'] = True
        if not Profile.objects.filter(user=self.request.user).first():
            context['has_profile'] = False

        return context

    def form_valid(self, form):
        form_instance = form.instance
        form_instance.user = self.request.user

        return super().form_valid(form)
