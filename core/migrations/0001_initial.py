# Generated by Django 3.2.12 on 2022-05-15 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import martor.models
import smart_selects.db_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('objective', martor.models.MartorField(blank=True, null=True)),
                ('project_information', martor.models.MartorField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short_description', models.TextField(blank=True, null=True)),
                ('description', martor.models.MartorField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('risk_score', models.IntegerField(default=5)),
                ('description', martor.models.MartorField()),
                ('solution', martor.models.MartorField()),
                ('more_info', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='project', chained_model_field='project', default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.report')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
                ('target', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='project', chained_model_field='project', on_delete=django.db.models.deletion.CASCADE, to='core.target')),
            ],
        ),
        migrations.CreateModel(
            name='DomainCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.URLField()),
                ('data', models.JSONField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
            ],
        ),
    ]
