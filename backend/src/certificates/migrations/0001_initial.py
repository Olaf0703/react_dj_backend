# Generated by Django 3.2.12 on 2022-05-03 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0003_auto_20220426_1914'),
        ('students', '0009_student_classroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('image', models.URLField(null=True)),
                ('pos_title', models.FloatField(null=True)),
                ('pos_editable_text', models.FloatField(null=True)),
                ('pos_student_name', models.FloatField(null=True)),
                ('pos_text', models.FloatField(null=True)),
                ('pos_name', models.FloatField(null=True)),
                ('pos_from_who', models.FloatField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentCertificates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('editableText', models.TextField(null=True)),
                ('text', models.TextField(null=True)),
                ('fromWho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.teacher')),
                ('toWho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
