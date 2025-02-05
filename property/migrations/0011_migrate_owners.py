from django.db import migrations


def migrate_owners(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')

    for flat in Flat.objects.iterator():
        owner, created = Owner.objects.get_or_create(
            full_name=flat.owner,
            defaults={
                'phone_number': flat.owners_phonenumber,
                'normalized_phone': flat.owner_pure_phone,
            }
        )
        owner.flats.set([flat])


class Migration(migrations.Migration):
    dependencies = [
        ('property', '0010_owner'),
    ]

    operations = [
        migrations.RunPython(migrate_owners)
    ]
