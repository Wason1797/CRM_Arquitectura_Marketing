from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CampaignSerializer, ClientSerializer
from .models import Campaign, Client
import datetime as dt
from django.db.models import Q
from .functions import get_campaign_clients
from django.db.models import Count

# Create your views here.


class CampaignView(APIView):

    def post(self, request):
        try:
            updated_data = request.data
            updated_data['creation_date'] = dt.datetime.now().isoformat()
            updated_data['last_modification_date'] = updated_data['creation_date']
            updated_data['state'] = "C"
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
            return Response({"errors": e.args}, status=400)

    def get(self, request):
        try:
            return Response(CampaignSerializer(Campaign.objects.all(),
                                               many=True).data,
                            status=200)
        except Exception as e:
            return Response(data={"errors": e.args}, status=400)

    def put(self, request):
        try:
            updated_data = request.data
            campaignInstance = Campaign.objects.get(id=int(updated_data['id']))
            updated_data['last_modification_date'] = dt.datetime.now().isoformat()
            serializedCampaign = CampaignSerializer(
                campaignInstance, data=request.data, partial=True)
            if serializedCampaign.is_valid():
                serializedCampaign.save()
                return Response(status=201)
            else:
                return Response(status=400)
        except Exception as e:
            return Response(data={"errors": e.args}, status=400)


class CampaignLocationReportView(APIView):

    def get(self, request):
        state = request.GET.get('provincia')
        city = request.GET.get('canton')
        if state is None:
            return Response(data={"errors": "missing provincia filter"},
                            status=400)
        elif city is None:
            campaigns_by_location = Campaign.json_objects.filter_json(
                location__provincia=state)
        else:
            campaigns_by_location = Campaign.json_objects.filter_json(
                Q(location__provincia=state) &
                Q(location__canton=city))

        return Response(CampaignSerializer(campaigns_by_location, many=True).data,
                        status=200)


class ClientView(APIView):

    def get(self, request):
        return Response(data=ClientSerializer(Client.objects.all(), many=True).data,
                        status=200)


class ClientsTotalCampaignsReport(APIView):

    def get(self, request):
        clients_by_campaign = Client.objects.values('id', 'dni', 'email', 'full_name').annotate(
            total_campaigns=Count('campaignclients__campaign_id'))
        return Response(data=ClientSerializer(clients_by_campaign, many=True).data,
                        status=200)


class TelemarketingResultView(APIView):

    def put(self, request):
        pass
