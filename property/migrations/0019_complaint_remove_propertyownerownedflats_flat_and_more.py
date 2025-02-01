from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0018_owner_flats2_alter_flat_owner_pure_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint_text', models.TextField(verbose_name='Текст жалобы')),
            ],
        ),

        migrations.RemoveField(
            model_name='propertyownerownedflats',
            name='flat',
        ),
        migrations.RemoveField(
            model_name='propertyownerownedflats',
            name='owner',
        ),

        migrations.RemoveField(
            model_name='flat',
            name='owner_name',
        ),
        migrations.RemoveField(
            model_name='flat',
            name='owner_pure_phone',
        ),
        migrations.RemoveField(
            model_name='flat',
            name='owners_phonenumber',
        ),

        migrations.RemoveField(
            model_name='owner',
            name='flats2',
        ),

        migrations.AddField(
            model_name='owner',
            name='flat',
            field=models.ManyToManyField(related_name='flat_owners', to='property.flat', verbose_name='Квартиры в собственности'),
        ),

        migrations.RemoveField(
            model_name='flat',
            name='owners',
        ),

        migrations.AddField(
            model_name='flat',
            name='owners',
            field=models.ManyToManyField(blank=True, related_name='owners_of_flat', to='property.owner', verbose_name='Собственники'),
        ),

        migrations.DeleteModel(
            name='Complaints',
        ),
        migrations.DeleteModel(
            name='PropertyOwnerOwnedFlats',
        ),

        migrations.AddField(
            model_name='complaint',
            name='flat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='property.flat', verbose_name='Квартира, на которую пожаловались'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to=settings.AUTH_USER_MODEL, verbose_name='Кто жаловался'),
        ),
    ]