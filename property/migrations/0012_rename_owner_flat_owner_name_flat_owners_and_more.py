# Generated by Django 5.1.5 on 2025-01-19 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0011_migrate_owners'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flat',
            old_name='owner',
            new_name='owner_name',
        ),
        migrations.AddField(
            model_name='flat',
            name='owners',
            field=models.ManyToManyField(blank=True, related_name='flats_owned', to='property.owner'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='flats',
            field=models.ManyToManyField(blank=True, related_name='flats_with_owner', to='property.flat', verbose_name='Квартиры в собственности'),
        ),
    ]
