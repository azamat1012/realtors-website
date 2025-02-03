

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField






class Flat(models.Model):
    is_new_building = models.BooleanField(
        'Новостройка', null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True)

    description = models.TextField('Текст объявления', blank=True)
    price = models.IntegerField('Цена квартиры', db_index=True)

    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True)
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное')
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4')
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж')

    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True)
    living_area = models.IntegerField(
        'количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True)

    has_balcony = models.BooleanField(
        'Наличие балкона', null=True, blank=True, db_index=True)
    active = models.BooleanField('Активно-ли объявление', db_index=True)
    likes = models.ManyToManyField(
        User, related_name='liked_posts', blank=True, verbose_name='Лайки')
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True)
    owners = models.ManyToManyField("Owner", verbose_name='Собственники', blank=True, related_name='owners_of_flat')

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'


class Owner(models.Model):
    full_name = models.CharField('ФИО собственника', max_length=200)
    phone_number = models.CharField(
        'Номер телефона', max_length=20, blank=True, null=True)
    normalized_phone = PhoneNumberField(
        'Нормализованный номер владельца', blank=True, null=True)
    flat = models.ManyToManyField(
        Flat, related_name='owners', verbose_name='Квартиры в собственности')

    def __str__(self):
        return self.full_name

class Complaint(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Кто жаловался", related_name='complainant')
    flat = models.ForeignKey(
        Flat, on_delete=models.CASCADE,  verbose_name="Квартира, на которую пожаловались",related_name='complaints')

    complaint_text = models.TextField(verbose_name="Текст жалобы")

    def __str__(self):
        return f"Жалоба от {self.user} на квартиру {self.flat}"
    
