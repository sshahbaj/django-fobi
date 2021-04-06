from django.db import migrations
import uuid


def gen_uuid(apps, schema_editor):
    FormEntry = apps.get_model('fobi', 'FormEntry')
    for row in FormEntry.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('fobi', '0018_formentry_uuid'),
    ]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]