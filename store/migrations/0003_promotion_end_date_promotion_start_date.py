# Generated by Django 4.1.2 on 2022-10-20 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_collection_featured_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='end_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='start_date',
            field=models.DateField(auto_now=True),
        ),
        
    ]
