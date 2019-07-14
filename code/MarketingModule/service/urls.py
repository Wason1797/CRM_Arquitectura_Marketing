from .views import CampaignView, CampaignLocationReportView, ClientView, \
    ClientsTotalCampaignsReport, CampaignGenderReportView, ClientsByAdvisorView, \
    ClientsCampaignReportView, AdvisorView
from django.urls import path

urlpatterns = [
    path('campaign/', CampaignView.as_view()),
    path('client/', ClientView.as_view()),
    path('advisor/', AdvisorView.as_view()),
    path('campaign-location-report/', CampaignLocationReportView.as_view()),
    path('clients-total-campaign-report/', ClientsTotalCampaignsReport.as_view()),
    path('clients-advisor-report/', ClientsByAdvisorView.as_view()),
    path('clients-campaign-report/', ClientsCampaignReportView.as_view()),
    path('campaign-gender-report/', CampaignGenderReportView.as_view()),
]
