from django.db import models
from django.utils.text import slugify
from app.models import RandomSlugModel, TimestampModel, IsActiveModel
from payments.models import DiscountCode


class Group(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'group_'

    name = models.CharField(max_length=128, null=True)
    internal_code = models.CharField(max_length=128, null=True)
    population = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(editable=False)

    grade = models.ForeignKey(
        'kb.Grade', on_delete=models.PROTECT, null=True, blank=True)
    area_of_knowledges = models.ManyToManyField(
        'kb.AreaOfKnowledge', blank=True)
    school_personnel = models.ForeignKey(
        'organization.SchoolPersonnel', on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class School(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'school_'

    name = models.CharField(max_length=128, null=True)
    slug = models.SlugField(editable=False)
    internal_code = models.CharField(max_length=128, null=True)
    type_of = models.CharField(max_length=100, null=True)

    student_plan = models.ManyToManyField('plans.StudentPlan')
    organization = models.ForeignKey(
        'organization.Organization', on_delete=models.PROTECT, null=True)
    # student = models.ManyToManyField('students.Student', blank=True)
    # group = models.ManyToManyField('organization.Group', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class SchoolPersonnel(TimestampModel, RandomSlugModel, IsActiveModel):
    GENDER_MALE = 'MALE'
    GENDER_FEMALE = 'FEMALE'
    GENDER_OTHER = 'OTHER'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    )

    PREFIX = 'school_personnel_'

    user = models.OneToOneField(
        'users.User',
        on_delete=models.PROTECT,
        null=True
    )
    school = models.ForeignKey(
        'organization.School',
        on_delete=models.PROTECT,
        null=True
    )
    discountCode = models.ForeignKey(
        DiscountCode,
        on_delete=models.CASCADE,
        null=True
    )

    name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True)
    identification_number = models.CharField(max_length=128, null=True)
    position = models.CharField(max_length=128, null=True)
    zip = models.CharField(max_length=128, null=True)
    country = models.CharField(max_length=128, null=True)
    district = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name+' '+self.last_name

class AdministrativePersonnel(SchoolPersonnel):
    pass

class Teacher(SchoolPersonnel):
    pass

class Classroom(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'classroom_'
    name = models.CharField(max_length=128, null=True)
    grade = models.ForeignKey(
        'kb.Grade', on_delete=models.PROTECT)
    language = models.CharField(max_length=128, null=True)
    audience = models.ForeignKey(
        'audiences.Audience', on_delete=models.PROTECT)
    school = models.ForeignKey(School, null=True, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.PROTECT)
    enable_games = models.BooleanField(default=True)
    game_cost = models.IntegerField(blank=True, null=True)
    time_zone = models.CharField(max_length=128, null=True)
    monday_start = models.TimeField(null=True, editable=True)
    monday_end = models.TimeField(null=True, editable=True)
    tuesday_start = models.TimeField(null=True, editable=True)
    tuesday_end = models.TimeField(null=True, editable=True)
    wednesday_start = models.TimeField(null=True, editable=True)
    wednesday_end = models.TimeField(null=True, editable=True)
    thursday_start = models.TimeField(null=True, editable=True)
    thursday_end = models.TimeField(null=True, editable=True)
    friday_start = models.TimeField(null=True, editable=True)
    friday_end = models.TimeField(null=True, editable=True)
    saturday_start = models.TimeField(null=True, editable=True)
    saturday_end = models.TimeField(null=True, editable=True)
    sunday_start = models.TimeField(null=True, editable=True)
    sunday_end = models.TimeField(null=True, editable=True)

