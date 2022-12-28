from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site


class User(AbstractUser):
    language = models.CharField(
        max_length=64,
        choices=settings.LANGUAGES,
        blank=True,
        null=True,
    )
    # stripe_customer = models.ForeignKey(
    #     'djstripe.Customer',
    #     on_delete=models.PROTECT,
    #     blank=True,
    #     null=True,
    # )
    stripe_customer_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    # email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        current_site = Site.objects.get_current()

        if not self.language:
            self.language = settings.PARLER_LANGUAGES[current_site.id][0]['code']

        return super().save(*args, **kwargs)
