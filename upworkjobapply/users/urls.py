from django.urls import path

from users.views import (
    UserCreateView,

    AuthView,
    AuthLogoutView,

    ProfileView,
    ProfileCreateView,
    DelProfile,

    CheckCoverLeter,
    GenCoverLeter,
    ProposalHistory,
    ClearProposalHistory,
    CheckCoverHistory,
    ClearCheckCoverHistory,
)

app_name = "users"

urlpatterns = [
    path('signup', UserCreateView.as_view(), name='register'),
    path('auth/logout', AuthLogoutView.as_view(), name='logout'),
    path('auth/login', AuthView.as_view(), name='login'),

]

urlpatterns += [
    path('profile-dash', ProfileView.as_view(), name='profile-dash'),
    path('profile-delete', DelProfile.as_view(), name='profile-delete'),
    path('profile-create', ProfileCreateView.as_view(), name='profile-create'),

]

urlpatterns += [
    path('check-proposal-history/del-all',
         ClearCheckCoverHistory.as_view(), name='check-proposal-del'),
    path('check-proposal-history', CheckCoverHistory.as_view(),
         name='check-proposal-history'),

    path('proposal-history/del-all',
         ClearProposalHistory.as_view(), name='proposal-del'),
    path('proposal-history', ProposalHistory.as_view(), name='proposal-history'),
    path('check-cover-leter', CheckCoverLeter.as_view(), name='check-cover'),
    path('gen-cover-leter', GenCoverLeter.as_view(), name='gen-cover'),

]
