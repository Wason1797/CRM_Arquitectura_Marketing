from .views import CampaignView, CampaignLocationReportView, ClientView, \
    ClientsTotalCampaignsReport, CampaignGenderReportView, ClientsByAdvisorView, \
    ClientsCampaignReportView, AdvisorView, CalculateRiskView, TelemarketingResultView,\
    SendEmails
from django.urls import path

urlpatterns = [
    path('campaign/', CampaignView.as_view()),
    path('client/', ClientView.as_view()),
    path('advisor/', AdvisorView.as_view()),
    path('campaign-location-report/', CampaignLocationReportView.as_view()),
    path('clients-total-campaign-report/', ClientsTotalCampaignsReport.as_view()),
    path('clients-campaign-advisor/', ClientsByAdvisorView.as_view()),
    path('clients-campaign-report/', ClientsCampaignReportView.as_view()),
    path('campaign-gender-report/', CampaignGenderReportView.as_view()),
    path('client-risk/', CalculateRiskView.as_view()),
    path('telemarketing-result/', TelemarketingResultView.as_view()),
    path('campaign-send-email/', SendEmails.as_view()),
]
