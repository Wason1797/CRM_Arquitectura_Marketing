from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CampaignSerializer, ClientSerializer, \
    AdvisorSerializer
from .models import Campaign, Client, Advisor
import datetime as dt
from django.db.models import Q
from .functions import get_campaign_clients, decode_token
from django.db.models import Count
from rest_framework.authentication import get_authorization_header


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
            campaign_id = request.GET.get('campaign_id')
            if campaign_id:
                campaing = Campaign.objects.get(id=int(campaign_id))
                return Response(data=CampaignSerializer(campaing).data,
                                status=200)
            else:
                return Response(CampaignSerializer(Campaign.objects.all(), many=True).data,
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


class AdvisorView(APIView):

    def get(self, request):
        return Response(data=AdvisorSerializer(Advisor.objects.all(), many=True).data, status=200)

    def post(self, request):
        serializedAdvisor = AdvisorSerializer(data=request.data, partial=True)
        if serializedAdvisor.is_valid():
            serializedAdvisor.save()
            return Response(status=201)
        else:
            return Response(serializedAdvisor.errors, status=400)


class CampaignLocationReportView(APIView):

    def get(self, request):
        province = request.GET.get('province')
        city = request.GET.get('city')
        if province is None:
            return Response(data={"errors": "missing province filter"},
                            status=400)
        elif city is None:
            campaigns_by_location = Campaign.json_objects.filter_json(
                location__provincia=province)
        else:
            campaigns_by_location = Campaign.json_objects.filter_json(
                Q(location__provincia=province) &
                Q(location__canton=city))

        return Response(CampaignSerializer(campaigns_by_location, many=True).data,
                        status=200)


class CampaignGenderReportView(APIView):

    def get(self, request):
        gender = request.GET.get('gender')
        if gender is None:
            return Response(data={"errors": "missing gender filter"},
                            status=400)
        else:
            campaigns_by_gender = Campaign.objects.filter(gender_range=gender)
            return Response(CampaignSerializer(campaigns_by_gender, many=True).data,
                            status=200)


class ClientView(APIView):

    def get(self, request):
        auth = get_authorization_header(request).split()
        print(decode_token(auth))
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


class ClientsCampaignReportView(APIView):

    def get(self, request):
        campaign_id = request.GET.get('campaign_id')
        if campaign_id is None:
            return Response(data={"errors": "missing campaign id filter"},
                            status=400)
        else:
            clients = Client.objects.filter(campaign__id=int(campaign_id))
            return Response(data=ClientSerializer(clients, many=True).data,
                            status=200)


class ClientsByAdvisorView(APIView):

    def get(self, request):
        advisor_id = request.GET.get('advisor_id')
        if advisor_id:
            clients = Client.objects.filter(telemarketingresult__advisor__id=int(advisor_id))
            return Response(data=ClientSerializer(clients, many=True).data,
                            status=200)
        else:
            return Response(data={"errors": "missing advisor id filter"},
                            status=400)
