from django.db import migrations
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


def autofill_phonenumbers(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')

    for flat in Flat.objects.iterator():
        if flat.owners_phonenumber:
            try:
                # Парсим номер
                parsed_number = phonenumbers.parse(
                    flat.owners_phonenumber, 'RU')

                # Проверяем валидность номера
                if phonenumbers.is_valid_number(parsed_number):
                    normalized_phone = phonenumbers.format_number(
                        parsed_number, phonenumbers.PhoneNumberFormat.E164)

                    # Проверяем, не существует ли такой номер в базе данных
                    if not Flat.objects.filter(owner_pure_phone=normalized_phone).exists():
                        flat.owner_pure_phone = normalized_phone
                        flat.save()
            except NumberParseException:
                continue


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_flat_owner_pure_phone'),
    ]

    operations = [
        migrations.RunPython(autofill_phonenumbers)
    ]
