from rest_framework.serializers import ModelSerializer, JSONField, \
    DecimalField, EmailField, ChoiceField, IntegerField, DateField
from .models import Campaign, Client, Advisor, TelemarketingResult


class CampaignSerializer(ModelSerializer):

    location = JSONField()
    publicity_configuration = JSONField()
    products = JSONField()
    budget = DecimalField(max_digits=12, decimal_places=3)
    gender_range = ChoiceField(choices=['M', 'F', 'M-F'])

    class Meta:
        model = Campaign
        exclude = ('clients',)


class ClientSerializer(ModelSerializer):

    location = JSONField(required=False)
    email = EmailField()
    earnings = DecimalField(max_digits=9, decimal_places=2, required=False)
    gender = ChoiceField(choices=['M', 'F'], required=False)
    total_campaigns = IntegerField(required=False)
    birth_date = DateField(required=False)

    class Meta:
        model = Client
        fields = '__all__'


class AdvisorSerializer(ModelSerializer):

    class Meta:

        model = Advisor
        fields = '__all__'


class TelemarketingResultSerializer(ModelSerializer):

    class Meta:

        model = TelemarketingResult
        fields = '__all__'
