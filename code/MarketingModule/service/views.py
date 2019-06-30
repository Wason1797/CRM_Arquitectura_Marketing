from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CampaignSerializer
from .models import Campaign
import datetime as dt
from .functions import get_campaign_clients

# Create your views here.


class CampaignView(APIView):

    def post(self, request):
        try:
            updated_data = request.data
            updated_data['creation_date'] = dt.datetime.now().isoformat()
            updated_data['last_modification_date'] = updated_data['creation_date']
            serializedCampaign = CampaignSerializer(
                data=updated_data, partial=True)
            if serializedCampaign.is_valid():
                campaign = serializedCampaign.save()
                campaign.client_set.add(get_campaign_clients(
                    updated_data['age_range']
                    # TODO consume the api and get all clients
                ))
                return Response(status=201)
            else:
                return Response(serializedCampaign.errors, status=400)
        except Exception as e:
            return Response(e.__dict__, status=400)

    def get(self, request):
        return Response(CampaignSerializer(Campaign.objects.all(), many=True).data, status=200)

    def put(self, request):
        campaignInstance = Campaign.objects.get(id=int(request.data['id']))
        serializedCampaign = CampaignSerializer(
            campaignInstance, data=request.data, partial=True)
        if serializedCampaign.is_valid():
            serializedCampaign.save()
            return Response(status=201)
        else:
            return Response(status=400)
