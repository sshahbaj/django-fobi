# Generated by Django 3.1.7 on 2021-03-30 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fobi_contrib_plugins_form_handlers_db_store', '0002_savedformwizarddataentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedformdataentry',
            name='metadata',
            field=models.JSONField(null=True),
        ),
    ]
