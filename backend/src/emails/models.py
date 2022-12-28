from django.db import models


class SubscriptionType(models.Model):
    name = models.CharField(max_length=64)


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.PROTECT)
    subscription_type = models.ManyToManyField(SubscriptionType, blank=True)
