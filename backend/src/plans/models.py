from django.db import models
from django.utils.text import slugify
from app.models import RandomSlugModel, TimestampModel, IsActiveModel


class Plan(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'plan_'

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    area_of_knowledge = models.CharField(max_length=255, choices=(
        ("ALL", "ALL"), ("ONE", "ONE"), ("TWO", "TWO")), default="ALL")
    slug = models.SlugField(editable=False)
    price_month = models.DecimalField(
        max_digits=15, decimal_places=2, default=0)
    price_year = models.DecimalField(
        max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=4)
    stripe_monthly_plan_id = models.CharField(max_length=255, blank=True)
    stripe_monthly_plan_half_price_id = models.CharField(
        max_length=255, blank=True)
    stripe_yearly_plan_id = models.CharField(max_length=255, blank=True)
    stripe_yearly_plan_half_price_id = models.CharField(
        max_length=255, blank=True)
    is_cancel = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class GuardianStudentPlan(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'guardian_plan_'

    guardian = models.ForeignKey(
        'guardians.Guardian', on_delete=models.PROTECT)
    student = models.OneToOneField(
        'students.Student', on_delete=models.PROTECT, blank=True, null=True)
    order_detail = models.ForeignKey(
        'payments.OrderDetail', on_delete=models.CASCADE)
    slug = models.SlugField(editable=False)
    plan = models.ForeignKey('Plan', on_delete=models.PROTECT, blank=True)
    subject = models.ManyToManyField(
        'kb.AreaOfKnowledge',
        blank=True
    )
    cancel_reason = models.TextField(blank=True)
    is_cancel = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True)
    period = models.CharField(
        max_length=100,
        choices=(("MONTHLY", "Monthly"), ("YEARLY", "Yearly")),
        default="MONTHLY"
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return str(self.id)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)


class StudentPlan(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'student_plan_'

    name = models.CharField(max_length=128)
    slug = models.SlugField(editable=False)
    audience = models.ForeignKey(
        'audiences.Audience',
        on_delete=models.PROTECT,
    )
    topic_grade = models.ManyToManyField(
        'kb.TopicGrade',
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
