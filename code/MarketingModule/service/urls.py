from .views import CampaignView, CampaignLocationReportView, ClientView, \
    ClientsTotalCampaignsReport, CampaignGenderReportView
from django.urls import path

urlpatterns = [
    path('campaign/', CampaignView.as_view()),
    path('client/', ClientView.as_view()),
    path('campaign-location-report/', CampaignLocationReportView.as_view()),
    path('clients-campaign-report/', ClientsTotalCampaignsReport.as_view()),
    path('campaign-gender-report/', CampaignGenderReportView.as_view()),
]
