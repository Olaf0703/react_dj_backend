# Generated by Django 3.2.12 on 2022-03-17 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20220314_1220'),
        ('plans', '0004_auto_20220314_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardianstudentplan',
            name='student',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='students.student'),
        ),
    ]
