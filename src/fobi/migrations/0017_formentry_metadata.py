# Generated by Django 3.1.7 on 2021-03-30 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fobi', '0016_formentry_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='formentry',
            name='metadata',
            field=models.JSONField(null=True),
        ),
    ]