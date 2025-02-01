from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0013_connect_owners_and_flats'),
    ]

    operations = [
        # Remove the old owners field
        migrations.RemoveField(
            model_name='flat',
            name='owners',
        ),
        # Create the intermediate through model
        migrations.CreateModel(
            name='PropertyOwnerOwnedFlats',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 to='property.flat', verbose_name='Квартира')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 to='property.owner', verbose_name='Собственник')),
            ],
            options={
                'verbose_name': 'Связь собственник-квартира',
                'verbose_name_plural': 'Связи собственник-квартира',
                'unique_together': {('owner', 'flat')},
            },
        ),
        # Add the new owners field with the through table
        migrations.AddField(
            model_name='flat',
            name='owners',
            field=models.ManyToManyField(
                related_name='flats_owned',
                through='property.PropertyOwnerOwnedFlats',
                to='property.owner',
            ),
        ),
    ]
