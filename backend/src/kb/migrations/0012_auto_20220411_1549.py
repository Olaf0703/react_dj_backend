# Generated by Django 3.2.12 on 2022-04-11 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kb', '0011_remove_answeroption_tts_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multiplechoiceansweroption',
            name='is_correct',
        ),
        migrations.RemoveField(
            model_name='multipleselectansweroption',
            name='is_correct',
        ),
        migrations.RemoveField(
            model_name='typeinansweroption',
            name='is_correct',
        ),
        migrations.AddField(
            model_name='answeroption',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]
