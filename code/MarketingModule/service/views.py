from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CampaignSerializer, ClientSerializer, \
    AdvisorSerializer, TelemarketingResultSerializer
from .models import Campaign, Client, Advisor, TelemarketingResult
import datetime as dt
from django.db.models import Q
from .functions import calculate_risk, get_campaign_clients, get_list_chunks, get_file_from_s3_service
from django.db.models import Count


class CampaignView(APIView):

    def post(self, request):
        try:
            updated_data = request.data
            updated_data['last_modification_date'] = dt.datetime.now()
            updated_data['state'] = "C"
            advisors = updated_data['advisors']
            del updated_data['advisors']
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

                client_chunks = list(get_list_chunks(db_clients, len(advisors)))
                sliced_db_clients = zip(client_chunks, advisors)
                del client_chunks

                telemarketing_results = []
                for client_chunk, advisor in sliced_db_clients:
                    for client in client_chunk:
                        telemarketing_results.append({
                            'client': client.id,
                            'campaign': campaign.id,
                            'advisor': advisor,
                            'created_by': campaign.created_by,
                            'modified_by': campaign.modified_by
                        })

                serialized_telemarketing = TelemarketingResultSerializer(data=telemarketing_results, many=True)
                if serialized_telemarketing.is_valid():
                    serialized_telemarketing.save()
                else:
                    print(serialized_telemarketing.errors)

                return Response(status=201)
            else:
                return Response(serialized_campaign.errors, status=400)
        except Exception as e:
            return Response(data={"errors": str(e)}, status=500)

    def get(self, request):
        try:
            campaign_id = request.GET.get('campaign_id')
            created_by = request.GET.get('created_by')
            if campaign_id:
                campaing = Campaign.objects.get(id=int(campaign_id))
                return Response(data=CampaignSerializer(campaing).data,
                                status=200)
            elif created_by:
                return Response(CampaignSerializer(Campaign.objects.filter(created_by=int(created_by)), many=True).data,
                                status=200)
            else:
                return Response(CampaignSerializer(Campaign.objects.all(), many=True).data,
                                status=200)
        except Exception as e:
            return Response(data={"errors": str(e)}, status=500)

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
            return Response(data={"errors": str(e)}, status=500)


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
        created_by = request.GET.get('created_by')
        province = request.GET.get('province')
        city = request.GET.get('city')
        if province is None and created_by:
            result = dict()
            campaigns = Campaign.json_objects.filter(created_by=int(created_by))
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
                Q(location__provincia=province) &
                Q(created_by=created_by))
        else:
            campaigns_by_location = Campaign.json_objects.filter_json(
                Q(location__provincia=province) &
                Q(location__canton=city) &
                Q(created_by=created_by))

        return Response(CampaignSerializer(campaigns_by_location, many=True).data,
                        status=200)


class CampaignGenderReportView(APIView):

    def get(self, request):
        try:
            created_by = request.GET.get('created_by')
            gender = request.GET.get('gender')
            if gender and created_by:
                campaigns_by_gender = Campaign.objects.filter(Q(gender_range=gender) & Q(created_by=created_by))
                return Response(CampaignSerializer(campaigns_by_gender, many=True).data,
                                status=200)

            else:
                return Response(data={"errors": "missing gender or created by filters"},
                                status=400)
        except Exception as e:
            return Response(data={"errors": str(e)}, status=500)


class ClientView(APIView):

    def get(self, request):
        return Response(data=ClientSerializer(Client.objects.all(), many=True).data,
                        status=200)


class ClientsTotalCampaignsReport(APIView):

    def get(self, request):
        try:
            created_by = request.GET.get('created_by')
            clients_by_campaign = Client.objects.filter(campaign__created_by=int(created_by))\
                .values('id', 'dni', 'email', 'full_name').annotate(
                total_campaigns=Count('campaignclients__campaign_id')).order_by('-total_campaigns')[:10]
            return Response(data=ClientSerializer(clients_by_campaign, many=True).data,
                            status=200)
        except Exception as e:
            return Response(data={"errors": str(e)}, status=500)


class TelemarketingResultView(APIView):

    def get(self, request):

        try:
            created_by = request.GET.get('created_by')
            return Response(data=TelemarketingResultSerializer(
                TelemarketingResult.objects.filter(campaign__created_by=created_by), many=True).data, status=200)
        except Exception as e:
            return Response(data={"errors": str(e)}, status=500)

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
            return Response(data={"errors": str(e)}, status=500)


class ClientsCampaignReportView(APIView):

    def get(self, request):
        try:
            campaign_id = request.GET.get('campaign_id')
            if campaign_id is None:
                return Response(data={"errors": "missing campaign id filter"},
                                status=400)
            else:
                clients = Client.objects.filter(campaign__id=int(campaign_id))
                return Response(data=ClientSerializer(clients, many=True).data,
                                status=200)
        except Exception as e:
            return Response(data={"errors": str(e)}, status=500)


class ClientsByAdvisorView(APIView):

    def get(self, request):
        try:
            advisor_id = request.GET.get('advisor_id')
            campaign_id = request.GET.get('campaign_id')
            if advisor_id:
                clients = Client.objects.filter(
                    Q(telemarketingresult__advisor__id=int(advisor_id)) &
                    Q(telemarketingresult__campaign__id=int(campaign_id)))
                return Response(data=ClientSerializer(clients, many=True).data,
                                status=200)
            else:
                return Response(data={"errors": "missing advisor or campaign id filter"},
                                status=400)
        except Exception as e:
            return Response(data={"errors": str(e)}, status=500)


class CalculateRiskView(APIView):

    def get(self, request):
        try:
            dni = request.GET.get('dni')

            client = Client.objects.get(dni=dni)
            risk = calculate_risk(client, 'localhost')
            return Response(data=dict({'risk': risk}, **ClientSerializer(client).data))
        except Exception as e:
            return Response(data={"errors": str(e)}, status=500)


class SendEmails(APIView):

    def get(self, request):
        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            campaign_id = request.GET.get('campaign_id')

            if campaign_id:
                campaign = Campaign.json_objects.get(id=int(campaign_id))
                clients = campaign.clients.all()

                _from = 'arquitecturacrm@gmail.com'
                _pwd = 'ArquitecturaSW.2019'

                _mail_server = 'smtp.gmail.com'
                _port = 587

                msg = MIMEMultipart('alternative')
                msg['Subject'] = 'Publicity test'
                msg['From'] = _from

                relative_path = campaign.publicity_configuration.get('path')

                path = get_file_from_s3_service(
                    'http://18.207.118.94:3000/documentfolder/14{}/alex'.format(relative_path))

                with open(path, mode='r', encoding='utf-8') as html:
                    html_string = html.read()

                content = MIMEText(html_string, 'html')

                msg.attach(content)

                already_sent = set()

                for client in clients:
                    if client.email not in already_sent:
                        already_sent.add(client.email)

                smtp = smtplib.SMTP(host=_mail_server, port=_port)
                smtp.starttls()
                smtp.login(_from, _pwd)

                msg['To'] = ','.join(already_sent)
                smtp.send_message(msg)
                del msg
                del already_sent
                smtp.quit()

                return Response(data={'message': 'emails sent'}, status=200)
            else:
                return Response(data={'errors': 'campaign id filter missing'}, status=400)
        except Exception as e:
            return Response(data={"errors": str(e)}, status=500)
