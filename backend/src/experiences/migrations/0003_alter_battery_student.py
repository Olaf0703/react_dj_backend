# Generated by Django 3.2.12 on 2022-03-29 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_student_audience'),
        ('experiences', '0002_battery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battery',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='battery', to='students.student'),
        ),
    ]
