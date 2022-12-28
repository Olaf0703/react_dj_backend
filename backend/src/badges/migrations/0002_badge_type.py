# Generated by Django 3.2.12 on 2022-05-04 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='type',
            field=models.CharField(choices=[('Gold', 'Gold'), ('Silver', 'Silver'), ('Bronze', 'Bronze')], max_length=128, null=True),
        ),
    ]
