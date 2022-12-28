from django.db import models
from users.models import User
from students.models import Student
from guardians.models import Guardian
from django.db.models.signals import post_save
from django.dispatch import receiver


active_roles = (
    ("user", "user"),
    ("manager", "manager"),
    ("guardian", "guardian"),
    ("student", "student")
)


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=120, choices=active_roles, default="user")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = "user"

        if instance.is_staff:
            role = "manager"

        profile.objects.create(user=instance, role=role)


@receiver(post_save, sender=Guardian)
def create_guardian_profile(sender, instance, created, **kwargs):
    if created:
        student_profile = profile.objects.get(user=instance.user)
        student_profile.role = "guardian"
        student_profile.save()


@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        student_profile = profile.objects.get(user=instance.user)
        student_profile.role = "student"
        student_profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
