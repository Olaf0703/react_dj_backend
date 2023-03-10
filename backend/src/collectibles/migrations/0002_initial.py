# Generated by Django 3.2.12 on 2022-03-09 02:36

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0002_student_user'),
        ('collectibles', '0001_initial'),
        ('wallets', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StudentCollectible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('amount', models.IntegerField(default=1)),
                ('collectible', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='collectibles.collectible')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='students.student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CollectiblePurchaseTransaction',
            fields=[
                ('withdraw_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wallets.withdraw')),
                ('collectible', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='collectibles.collectible')),
            ],
            options={
                'abstract': False,
            },
            bases=('wallets.withdraw',),
        ),
        migrations.CreateModel(
            name='CollectiblePackPurchaseTransaction',
            fields=[
                ('withdraw_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wallets.withdraw')),
                ('collectible_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='collectibles.collectiblecategory')),
                ('collectibles', models.ManyToManyField(blank=True, to='collectibles.Collectible')),
            ],
            options={
                'abstract': False,
            },
            bases=('wallets.withdraw',),
        ),
        migrations.AddField(
            model_name='collectibledescription',
            name='collectible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collectibles.collectible'),
        ),
        migrations.AddField(
            model_name='collectibledescription',
            name='description',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collectibles.description'),
        ),
        migrations.AddField(
            model_name='collectiblecategorytranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='collectibles.collectiblecategory'),
        ),
        migrations.AddField(
            model_name='collectiblecategory',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sub_categories', to='collectibles.collectiblecategory'),
        ),
        migrations.AddField(
            model_name='collectible',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='collectibles.collectiblecategory'),
        ),
        migrations.AddField(
            model_name='collectible',
            name='description',
            field=models.ManyToManyField(through='collectibles.CollectibleDescription', to='collectibles.Description'),
        ),
        migrations.CreateModel(
            name='DescriptionTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('key', models.CharField(blank=True, max_length=32, null=True)),
                ('value', models.TextField()),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='collectibles.description')),
            ],
            options={
                'verbose_name': 'description Translation',
                'db_table': 'collectibles_description_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CollectibleTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=128, null=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='collectibles.collectible')),
            ],
            options={
                'verbose_name': 'collectible Translation',
                'db_table': 'collectibles_collectible_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='collectiblecategorytranslation',
            unique_together={('language_code', 'master')},
        ),
    ]
