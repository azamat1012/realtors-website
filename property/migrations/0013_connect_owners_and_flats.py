from django.db import migrations


def connect_owners_and_flats(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')

    for flat in Flat.objects.all().iterator():
        if flat.owners.exists():
            continue
        owner, created = Owner.objects.get_or_create(
            full_name='Неизвестно',
            defaults={
                'phone_number': 'Неизвестно',
                'normalized_phone': None,
            }
        )
        flat.owners.add(owner)


class Migration(migrations.Migration):
    dependencies = [
        ('property', '0012_rename_owner_flat_owner_name_flat_owners_and_more'),
    ]
    operations = [
        migrations.RunPython(connect_owners_and_flats)
    ]
