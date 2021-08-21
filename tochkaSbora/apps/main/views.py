from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import User, user_by_token, CollectionPlace, Market, MarketItem

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import os
from urllib.parse import unquote


APP_TOKEN = 'PX6eUmgv4th7GKqhqDr8E5AZt8SFi2Ja'

BLOCK_SIZE = 16

ENCRYPT_PWD = 'pN4a4JZEWED9ZiKTx956piXhaqweiV85'

def unpad(s):
    return s[:-ord(s[len(s) - 1:])]


def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def decrypt(enc):
    private_key = hashlib.sha256(ENCRYPT_PWD.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return json.loads(unpad(cipher.decrypt(enc[16:])))


def encrypt(raw):
    private_key = hashlib.sha256(ENCRYPT_PWD.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode("utf-8"))).decode(encoding="utf-8")


class APIViewBase(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, format=None):
        self.query_params = self.request.query_params #decrypt(unquote(self.request.query_params.get("data", '')))
        self.data = dict()

        app_token = self.query_params.get('app_token', '')

        if APP_TOKEN == app_token:
            self.on_get()
        else:
            self.data = {'success': False}

        st = json.dumps(self.data)

        return Response(self.data) #{'data': encrypt(st)})

    def on_get(self):
        pass

    def post(self, format=None):
        self.query_params = self.request.query_params # decrypt(unquote(self.request.query_params.get("data", '')))
        self.data = dict()

        self.on_post()

        st = json.dumps(self.data)

        return Response(self.data) #{'data': encrypt(st)})

    def on_post(self):
        pass


class CreateUserAPI(APIViewBase):
    def on_get(self):
        user = None

        try:
            phone = self.query_params['phone']
            first_name = self.query_params['first_name']
            last_name = self.query_params['last_name']
            patronymic = self.query_params['patronymic']

            user = User.objects.get(
                phone_number=phone,
            )
            user.first_name = first_name
            user.last_name = last_name
            user.patronymic = patronymic
            user.save()

            success = True

        except:
            success = False


        self.data = {
            'user_id': user.id if user else -1,
            'success': success
        }


class GetUserQRTokenAPI(APIViewBase):
    def on_get(self):
        try:
            success = True

            token = self.query_params.get('token', '')

            user = user_by_token(token)

            qr_token = user.qr_token
        except:
            qr_token = ''
            success = False

        self.data = {
            'qr_token': qr_token,
            'success': success
        }


class TryAuthenticationAPI(APIViewBase):
    def on_get(self):
        try:
            success = True
            phone = self.query_params.get('phone', '')


            try:
                user = get_object_or_404(User, phone_number=phone)
                user_founded = True
            except:
                # не нашли, регистрируем
                user = User.objects.create(phone_number=phone, first_name='Имя', last_name='Фамилия', patronymic='Отчество')
                user_founded = False
            user.regenerate_passcode()

        except:
          user_founded = False
          success = False

        self.request.session['user_founded'] = user_founded

        self.data = {
            'user_founded': user_founded,
            'success': success,
        }


class InitAuthenticationAPI(APIViewBase):
    def on_get(self):
        try:
            success = True

            phone = self.query_params.get('phone', '-1')

            user = get_object_or_404(User, phone_number=phone)

            user.regenerate_passcode()

        except:
            success = False

        self.data = {
            'user_founded': self.request.session.get('user_founded', True),
            'success': success,
        }


class AuthenticateUserAPI(APIViewBase):
    def on_get(self):
        phone = self.query_params.get('phone', '')
        passcode = self.query_params.get('passcode', -1)

        try:
            user = get_object_or_404(User, phone_number=phone)

            if user and user.compare_passcode(passcode):
                token = user.regenerate_token()
                user.reset_passcode()

                success = True
            else:
                token = ''
                success = False

        except:
            success = False

        self.data = {
            'token': token,
            'success': success
        }


class UserInfoAPI(APIViewBase):
    def on_get(self):
        info = dict()

        try:
            success = True
            user = user_by_token(self.query_params['token'])

            if not user:
                raise Exception()

            info['id'] = user.id
            info['first_name'] = user.first_name
            info['last_name'] = user.last_name
            info['patronymic'] = user.patronymic
            info['coins'] = user.coins

        except:
            success = False

        self.data = {
            'info': info,
            'success': success
        }


class UserGarbageInfoAPI(APIViewBase):
    def on_get(self):
        info = dict()

        try:
            success = True
            user = user_by_token(self.query_params['token'])

            if not user:
                raise Exception()

            info['cardboard'] = user.garb_cardboard
            info['wastepaper'] = user.garb_wastepaper
            info['glass'] = user.garb_glass
            info['plastic_lid'] = user.garb_plastic_lid
            info['aluminum_can'] = user.garb_aluminum_can
            info['plastic_bottle'] = user.garb_plastic_bottle
            info['plastic_mk2'] = user.garb_plastic_mk2
            info['plastic_mk5'] = user.garb_plastic_mk5

        except:
             success = False

        self.data = {
            'info': info,
            'success': success
        }


class CollectionPlacesInfoAPI(APIViewBase):
    def on_get(self):
        places = CollectionPlace.objects.all()

        data = []
        i = 0
        for place in places:
            data.append({
                "address": place.address,
                "snippet": place.snippet,
                "latitude": place.latitude,
                "longitude": place.longitude,
            })
            i += 1

        self.data['info'] = data


class MarketsInfoAPI(APIViewBase):
    def on_get(self):
        markets = Market.objects.all()

        data = []
        i = 0
        for place in markets:
            data.append({
                "address": place.address,
                "snippet": place.snippet,
                "latitude": place.latitude,
                "longitude": place.longitude,
            })
            i += 1

        self.data['info'] = data


class MarketItemsInfoAPI(APIViewBase):
    def on_get(self):
        market_items = MarketItem.objects.all()

        data = []
        i = 0
        for item in market_items:
            data.append({
                "id": item.id,
                "icon_link": item.icon_link,
                "name": item.name,
                "cost": item.cost,
            })
            i += 1

        self.data['info'] = data


class MarketItemInfoAPI(APIViewBase):
    def on_get(self):
        try:
            success = True
            id = self.query_params.get('id', '')

            item = MarketItem.objects.get(id=id)

            info = {
                'icon_link': item.icon_link,
                'name': item.name,
                'description': item.description,
                'cost': item.cost,
                'available': item.available,
            }
        except:
            success = False
            info = {}

        self.data = {
            'info': info,
            'success': success
        }