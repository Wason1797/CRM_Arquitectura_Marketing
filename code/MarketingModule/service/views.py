from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CampaignSerializer, ClientSerializer, \
    AdvisorSerializer, TelemarketingResultSerializer
from .models import Campaign, Client, Advisor, TelemarketingResult
import datetime as dt
from django.db.models import Q
from .functions import decode_token, calculate_risk, get_campaign_clients
from django.db.models import Count
from rest_framework.authentication import get_authorization_header


class CampaignView(APIView):

    def post(self, request):
        try:
            updated_data = request.data
            # updated_data['creation_date'] = dt.datetime.now().isoformat()
            updated_data['last_modification_date'] = dt.datetime.now()
            updated_data['state'] = "C"
            age_range = updated_data.get('age_range').split('-')
            earning_range = updated_data.get('earning_range').split('-')
            serialized_campaign = CampaignSerializer(
                data=updated_data, partial=True)
            if serialized_campaign.is_valid():
                clients = get_campaign_clients(
                    location=updated_data.get('location').get('provincia'),
                    gender=updated_data.get('gender_range'),
                    min_age=int(age_range[0]),
                    max_age=int(age_range[1]),
                    min_salary=earning_range[0],
                    max_salary=int(earning_range[1]))
                curated_clients = []
                for client in clients:
                    if not Client.objects.filter(dni=client.get('dni')).exists():
                        curated_clients.append(client)
                serialized_clients = ClientSerializer(data=curated_clients, many=True)
                if serialized_clients.is_valid():
                    serialized_clients.save()

                del curated_clients
                client_dnis = []
                for client in clients:
                    client_dnis.append(client.get('dni'))
                del clients

                db_clients = list(Client.objects.filter(dni__in=client_dnis))
                del client_dnis

                campaign = serialized_campaign.save()
                campaign.clients.set(db_clients)

                return Response(status=201)
            else:
                return Response(serialized_campaign.errors, status=400)
        except Exception as e:
            print(e)
            return Response({"errors": e.__dict__}, status=400)

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
            updated_data['last_modification_date'] = dt.datetime.now()
            serializedCampaign = CampaignSerializer(
                campaignInstance, data=updated_data, partial=True)
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
            result = dict()
            campaigns = Campaign.json_objects.all()
            for campaign in campaigns:
                if campaign.location.get('provincia') in result:
                    result[campaign.location.get('provincia')] += 1
                else:
                    result[campaign.location.get('provincia')] = 1
            result_list = []
            for key, value in result.items():
                result_list.append({
                    'province': key,
                    'ammount': value
                })
            return Response(data=result_list, status=200)
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
            total_campaigns=Count('campaignclients__campaign_id')).order_by('-total_campaigns')[:10]
        return Response(data=ClientSerializer(clients_by_campaign, many=True).data,
                        status=200)


class TelemarketingResultView(APIView):

    def get(self, request):
        return Response(data=TelemarketingResultSerializer(
            TelemarketingResult.objects.all(), many=True).data, status=200)

    def post(self, request):
        result_data = request.data
        # result_data['creation_date'] = dt.datetime.now().isoformat()
        serialized_result = TelemarketingResultSerializer(data=result_data, partial=True)
        if serialized_result.is_valid():
            serialized_result.save()
            return Response(status=201)
        else:
            return Response(serialized_result.errors, status=400)

    def put(self, request):
        try:
            updated_data = request.data
            telemarketing_instance = TelemarketingResult.objects.get(
                advisor__id=int(updated_data['advisor']),
                client__id=int(updated_data['client']),
                campaign__id=int(updated_data['campaign']))
            updated_data['last_call_date'] = dt.datetime.now().isoformat()
            serialized_result = TelemarketingResultSerializer(
                telemarketing_instance, data=updated_data, partial=True)
            if serialized_result.is_valid():
                serialized_result.save()
                return Response(status=201)
            else:
                return Response(status=400)
        except Exception as e:
            return Response(data={"errors": e.args}, status=400)


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


class CalculateRiskView(APIView):

    def get(self, request):
        dni = request.GET.get('dni')

        client = Client.objects.get(dni=dni)
        risk = calculate_risk(client, 'localhost')
        return Response(data=dict({'risk': risk}, **ClientSerializer(client).data))
