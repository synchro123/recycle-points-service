from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404
import random


# Рядовой пользователь
class User(models.Model):
    class Meta:
        verbose_name = 'Рядовой пользователь'
        verbose_name_plural = 'Рядовые пользователи'

    phone_number = models.CharField(max_length=30, verbose_name='Номер телефона')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')
    passcode = models.CharField(max_length=6, verbose_name='Код подтверждения')
    token = models.CharField(max_length=50, verbose_name='Ключ доступа')
    qr_token = models.CharField(max_length=50, verbose_name='QR Ключ доступа')
    coins = models.IntegerField(default=0, verbose_name='Монеты')

    # сданный мусор (x50 гр.)
    garb_cardboard = models.IntegerField(default=0, verbose_name='Картона (x50 гр.)')
    garb_wastepaper = models.IntegerField(default=0, verbose_name='Макулатуры (x50 гр.)')
    garb_glass = models.IntegerField(default=0, verbose_name='Стекла (x50 гр.)')
    garb_plastic_lid = models.IntegerField(default=0, verbose_name='Пластиковых крышечек (x50 гр.)')
    garb_aluminum_can = models.IntegerField(default=0, verbose_name='Алюминиевых банок (x50 гр.)')
    garb_plastic_bottle = models.IntegerField(default=0, verbose_name='ПЭТ-бутылок (x50 гр.)')
    garb_plastic_mk2 = models.IntegerField(default=0, verbose_name='Пластика маркировки «2» (x50 гр.)')
    garb_plastic_mk5 = models.IntegerField(default=0, verbose_name='Пластика маркировки «5» (x50 гр.)')

    def compare_passcode(self, passcode):
        return len(self.passcode) == 4 and self.passcode == passcode

    def regenerate_passcode(self):
        self.passcode = '1986' #''.join(map(str, random.sample(range(10), 4)))
        self.save()

    def reset_passcode(self):
        self.passcode = -1
        self.save()

    def regenerate_token(self):
        chars = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        token = ''.join(map(str, random.sample(list(chars), len(chars)))) + str(self.id)
        self.token = token
        self.save()
        return token

    def regenerate_qr_token(self):
        chars = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        token = ''.join(map(str, random.sample(list(chars), len(chars)))) + str(self.id)
        self.qr_token = token
        self.save()
        return token


def user_by_token(token):
    return get_object_or_404(User, token=token)

def user_by_qr_token(token):
    return get_object_or_404(User, qr_token=token)


class CollectionPlace(models.Model):
    class Meta:
        verbose_name = 'Место сбора мусора'
        verbose_name_plural = 'Места сбора мусора'

    address = models.CharField(default='', max_length=100, verbose_name="Адрес")
    snippet = models.CharField(default='', max_length=50, verbose_name="Режим работы")
    latitude = models.FloatField(default=0, verbose_name="Широта")
    longitude = models.FloatField(default=0, verbose_name="Долгота")


class Market(models.Model):
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    address = models.CharField(default='', max_length=100, verbose_name="Адрес")
    snippet = models.CharField(default='', max_length=50, verbose_name="Режим работы")
    latitude = models.FloatField(default=0, verbose_name="Широта")
    longitude = models.FloatField(default=0, verbose_name="Долгота")


class MarketItem(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    icon_link = models.TextField(verbose_name='Ссылка на иконку')
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    cost = models.IntegerField(verbose_name='Стоимость')

    available = models.BooleanField(default=True, verbose_name='Доступность')