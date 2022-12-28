from django.db import models
from django.utils.text import slugify
from app.models import RandomSlugModel, TimestampModel, IsActiveModel
from app.models import RandomSlugModel, TimestampModel, IsActiveModel, ActiveManager


PAYMENT_METHOD = (("CARD", "CARD"), ("PAYPAL", "PAYPAL"), ("APPLEPAY", "APPLEPAY"), ("FREE", "FREE"))


class Order(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'order_'

    guardian = models.ForeignKey('guardians.Guardian', on_delete=models.CASCADE)
    sub_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    discount_code = models.CharField(max_length=255, blank=True)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHOD, default="CARD")
    is_paid = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)


class OrderDetail(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'order_detail_'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    plan = models.ForeignKey('plans.Plan', on_delete=models.CASCADE)
    payment_method_plan_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    period = models.CharField(
        max_length=100,
        choices=(("MONTHLY", "Monthly"), ("YEARLY", "Yearly")),
        default="MONTHLY"
    )
    update_from_detail_id = models.IntegerField(default=0)
    status = models.CharField(max_length=255, blank=True, null=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    on_discount = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    expired_at = models.DateTimeField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    cancel_reason = models.TextField(blank=True)
    is_cancel = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)
    error_message = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)


class PaypalTransaction(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'paypal_transaction_'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    token_id = models.CharField(max_length=255)
    approve_link = models.TextField()
    capture_link = models.TextField()
    is_captured = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)


class CardTransaction(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'card_transaction_'

    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)
    approve_link = models.TextField()
    card_first_name = models.CharField(max_length=255, blank=True, null=True)
    card_last_name = models.CharField(max_length=255, blank=True, null=True)
    card_number = models.CharField(max_length=255, blank=True, null=True)
    card_exp_month = models.CharField(max_length=255, blank=True, null=True)
    card_exp_year = models.CharField(max_length=255, blank=True, null=True)
    card_cvc = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    post_code = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    is_captured = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)

class PaymentMethodManager(ActiveManager):
    pass

class PaymentMethod(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'payment_method_'

    guardian = models.ForeignKey('guardians.Guardian', on_delete=models.CASCADE)
    method = models.CharField(max_length=255, choices=PAYMENT_METHOD, default="CARD")
    card_first_name = models.CharField(max_length=255, blank=True, null=True)
    card_last_name = models.CharField(max_length=255, blank=True, null=True)
    card_number = models.CharField(max_length=255, blank=True, null=True)
    card_exp_month = models.CharField(max_length=255, blank=True, null=True)
    card_exp_year = models.CharField(max_length=255, blank=True, null=True)
    card_cvc = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    post_code = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)
    
    objects = PaymentMethodManager()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)


class DiscountCode(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'discount_code_'

    code = models.CharField(max_length=255, unique=True)
    percentage = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    trial_day = models.IntegerField(default=0)
    expired_at = models.DateTimeField()
    stripe_coupon_id = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)
