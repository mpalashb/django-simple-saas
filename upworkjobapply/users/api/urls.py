from django.urls import path
from users.api.views import (
    GenerateProposalAPIView, CheckScoreAPIView,
)


urlpatterns = [
    path('check-score', CheckScoreAPIView.as_view()),
    path('gen-proposal', GenerateProposalAPIView.as_view())
]
