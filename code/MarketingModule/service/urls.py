from .views import CampaignView, CampaignLocationReportView, ClientView, \
    ClientsTotalCampaignsReport
from django.urls import path

urlpatterns = [
    path('campaign/', CampaignView.as_view()),
    path('client/', ClientView.as_view()),
    path('campaign-location-reports/', CampaignLocationReportView.as_view()),
    path('clients-campaign-reports/', ClientsTotalCampaignsReport.as_view()),
]
