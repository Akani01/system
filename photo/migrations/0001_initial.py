# Generated by Django 5.0 on 2025-02-06 05:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('website_url', models.CharField(blank=True, max_length=2000, null=True)),
                ('gmail_url', models.CharField(blank=True, max_length=2000, null=True)),
                ('whatsapp_number', models.CharField(blank=True, max_length=20, null=True)),
                ('facebook_url', models.CharField(blank=True, max_length=300, null=True)),
                ('tiktok_url', models.CharField(blank=True, max_length=300, null=True)),
                ('zoom_url', models.CharField(blank=True, max_length=900, null=True)),
                ('microsoftTeam_url', models.CharField(blank=True, max_length=900, null=True)),
                ('location', models.CharField(blank=True, max_length=900, null=True)),
                ('twitter_url', models.CharField(blank=True, max_length=900, null=True)),
                ('playstore_url', models.CharField(blank=True, max_length=900, null=True)),
                ('linkedin_url', models.CharField(blank=True, max_length=900, null=True)),
                ('instagram_url', models.CharField(blank=True, max_length=900, null=True)),
                ('pinterest_url', models.CharField(blank=True, max_length=900, null=True)),
                ('youtube_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='job.category')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
            },
        ),
    ]
