# Generated by Django 5.0 on 2025-01-11 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_names', models.CharField(blank=True, max_length=2000, null=True)),
                ('age', models.CharField(blank=True, max_length=2000, null=True)),
                ('address', models.CharField(blank=True, max_length=2000, null=True)),
                ('qualifications', models.CharField(blank=True, max_length=2000, null=True)),
                ('motivation', models.TextField()),
                ('recent_jobs', models.CharField(blank=True, max_length=2000, null=True)),
                ('position', models.CharField(blank=True, max_length=2000, null=True)),
                ('marital_status', models.CharField(choices=[('SINGLE', 'SINGLE'), ('MARRIED', 'MARRIED'), ('UNKNOWN', 'UNKNOWN'), ('OTHER', 'OTHER')], max_length=50)),
                ('experience', models.CharField(blank=True, max_length=2000, null=True)),
                ('contacts', models.CharField(blank=True, max_length=2000, null=True)),
                ('whatsapp_no', models.CharField(blank=True, max_length=2000, null=True)),
                ('image', models.ImageField(default='default.png', null=True, upload_to='jobs/img/%y/%m/%d/')),
                ('cv', models.FileField(upload_to='jobs/cv/%y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('website_url', models.CharField(blank=True, max_length=2000, null=True)),
                ('whatsapp_number', models.CharField(blank=True, max_length=20, null=True)),
                ('facebook_url', models.CharField(blank=True, max_length=300, null=True)),
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
            ],
            options={
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
            },
        ),
    ]
