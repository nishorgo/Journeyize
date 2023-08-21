# Generated by Django 4.2.4 on 2023-08-19 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_manager', '0006_rename_itinerary_parent_itineraryentries_itinerary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itinerary',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='itinerary',
            name='start_date',
        ),
        migrations.AddField(
            model_name='itineraryentries',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
