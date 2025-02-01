from django.db import migrations
from django.db.models import F


def migrate_owners(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')
    FlatOwner = Flat.owners.through  

    owner_data = {}
    for flat in Flat.objects.all().iterator(chunk_size=1000):  
        if flat.owner:
            for owner_name in flat.owner.split(','):
                owner_name = owner_name.strip()
                if owner_name not in owner_data:
                    owner_data[owner_name] = []
                owner_data[owner_name].append(flat.id)

    owners = [Owner(full_name=name) for name in owner_data.keys()]
    Owner.objects.bulk_create(owners, ignore_conflicts=True)  

    owner_name_to_id = {owner.full_name: owner.id for owner in Owner.objects.filter(full_name__in=owner_data.keys())}

    flat_owners = []
    for owner_name, flat_ids in owner_data.items():
        owner_id = owner_name_to_id[owner_name]
        flat_owners.extend([FlatOwner(flat_id=flat_id, owner_id=owner_id) for flat_id in flat_ids])

    FlatOwner.objects.bulk_create(flat_owners)


class Migration(migrations.Migration):
    dependencies = [
        ('property', '0010_owner'),
    ]

    operations = [
        migrations.RunPython(migrate_owners)
    ]