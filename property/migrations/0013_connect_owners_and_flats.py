from django.db import migrations


def connect_owners_and_flats(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')
    FlatOwner = Flat.owners.through  

    owner_data = {}
    for flat in Flat.objects.all().iterator(chunk_size=1000):  
        owner_name = flat.owner_name.strip() if flat.owner_name else None
        owner_phone = flat.owners_phonenumber.strip() if flat.owners_phonenumber else None
        normalized_phone = flat.owner_pure_phone

        if owner_name and owner_phone:
            owner_key = (owner_name, owner_phone, normalized_phone)
            if owner_key not in owner_data:
                owner_data[owner_key] = []
            owner_data[owner_key].append(flat.id)

    owners = [
        Owner(full_name=name, phone_number=phone, normalized_phone=normalized_phone)
        for (name, phone, normalized_phone) in owner_data.keys()
    ]
    Owner.objects.bulk_create(owners, ignore_conflicts=True)  

    owner_key_to_id = {
        (owner.full_name, owner.phone_number, owner.normalized_phone): owner.id
        for owner in Owner.objects.filter(
            full_name__in=[name for (name, _, _) in owner_data.keys()],
            phone_number__in=[phone for (_, phone, _) in owner_data.keys()],
        )
    }
    flat_owners = []
    for owner_key, flat_ids in owner_data.items():
        owner_id = owner_key_to_id[owner_key]
        flat_owners.extend([FlatOwner(flat_id=flat_id, owner_id=owner_id) for flat_id in flat_ids])

    FlatOwner.objects.bulk_create(flat_owners)


class Migration(migrations.Migration):
    dependencies = [
        ('property', '0012_rename_owner_flat_owner_name_flat_owners_and_more'),
    ]

    operations = [
        migrations.RunPython(connect_owners_and_flats)
    ]