from django.db import models
from oracle_json_field.fields import JSONField
from oracle_json_field.encoders import JSONEncoder
from oracle_json_field.managers import JsonQueryManager
from django.utils import timezone

# Create your models here


class Client(models.Model):
    dni = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=256)
    email = models.CharField(max_length=128)
    earnings = models.DecimalField(
        max_digits=9, decimal_places=2)
    birth_date = models.DateField()
    gender = models.CharField(max_length=3)
    location = JSONField(encoder=JSONEncoder)

    objects = models.Manager()
    json_objects = JsonQueryManager()


class Campaign(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    gender_range = models.CharField(max_length=20)
    age_range = models.CharField(max_length=10)
    earning_range = models.CharField(max_length=25)
    location = JSONField(encoder=JSONEncoder)
    publicity_configuration = JSONField(encoder=JSONEncoder)
    created_by = models.BigIntegerField()
    modified_by = models.BigIntegerField()
    creation_date = models.DateTimeField(default=timezone.now)
    last_modification_date = models.DateTimeField()
    state = models.CharField(max_length=3)
    stage = models.CharField(max_length=3)
    budget = models.DecimalField(
        max_digits=12, decimal_places=3)
    products = JSONField(encoder=JSONEncoder)
    clients = models.ManyToManyField(Client, through='CampaignClients')

    objects = models.Manager()
    json_objects = JsonQueryManager()


class CampaignClients(models.Model):
    date_added = models.DateTimeField(default=timezone.now)
    campaign = models.ForeignKey(Campaign, models.PROTECT)
    client = models.ForeignKey(Client, models.PROTECT)

    objects = models.Manager()


class Advisor(models.Model):
    user_name = models.CharField(max_length=128)

    objects = models.Manager()


class TelemarketingResult(models.Model):
    campaign = models.ForeignKey(Campaign, models.PROTECT)
    client = models.ForeignKey(Client, models.PROTECT)
    advisor = models.ForeignKey(Advisor, models.PROTECT)
    result = models.CharField(max_length=10, blank=True)
    client_risk = models.CharField(max_length=10, blank=True)
    creation_date = models.DateTimeField(default=timezone.now)
    last_call_date = models.DateTimeField(null=True, blank=True)
    created_by = models.BigIntegerField()
    modified_by = models.BigIntegerField()
    result_detail = models.TextField(blank=True)

    objects = models.Manager()
