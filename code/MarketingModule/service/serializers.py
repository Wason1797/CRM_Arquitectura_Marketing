from rest_framework.serializers import ModelSerializer, JSONField
from .models import Campaign


class CampaignSerializer(ModelSerializer):

    location = JSONField()
    publicity_configuration = JSONField()
    products = JSONField()

    class Meta:
        model = Campaign
        exclude = ('clients',
                   'state')
