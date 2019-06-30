from .views import CampaignView
from django.urls import path

urlpatterns = [
    path('campaign/', CampaignView.as_view()),
]
