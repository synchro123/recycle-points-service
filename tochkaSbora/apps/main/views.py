from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import User, user_by_token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

APP_TOKEN = ''


def generate_keys():
    """Генерирует приватный и публичный ключи"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    serial_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    serial_pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return serial_private, serial_pub


class APIViewBase(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, format=None):
        self.query_params = self.request.query_params
        self.data = dict()

        self.on_get()

        return Response(self.data)

    def on_get(self):
        pass

    def read_private(self, key):
        """Читает приватный ключ"""
        private_key = serialization.load_pem_private_key(
            key,
            password=None,
            backend=default_backend()
        )
        return private_key

    def decrypt(self, data):
        """Дешифрует сообщение, закодированное публичным ключом"""
        private_key = self.read_private(self.request.session['private_key'])  # self.read_private(bytes(self.request.session['private_key'], encoding="utf-8"))

        if not private_key:
            return ''

        decrypted = private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted

    def get_coder(self):
        key = self.request.session['sync_key']
        if key:
            return Fernet(bytes(key))
        else:
            return None


class CreateUserAPI(APIViewBase):
    def on_get(self):
        user = None

        # try:
        phone = self.query_params['phone']
        first_name = self.query_params['first_name']
        last_name = self.query_params['last_name']
        patronymic = self.query_params['patronymic']

        user = User.objects.create(
            phone_number=phone,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
        )

        success = True

    # except:
    #     success = False


''' self.data = {
     'user_id': user.id if user else -1,
     'success': success
 }'''


class InitSessionAPI(APIViewBase):
    def on_get(self):
        private_key, public_key = generate_keys()
        self.request.session['private_key'] = private_key.decode("utf-8")

        self.data = {
            'public_key': public_key.decode("utf-8"),
        }


class TryAuthenticationAPI(APIViewBase):
    def on_get(self):

        # try:
        key = self.decrypt(self.query_params.get('key', ''))
        if not key:
            raise Exception("ключ")
        self.request.session['sync_key'] = key

        phone = self.query_params.get('phone', '')

        print(phone, key)
        if not phone:
            raise Exception("телефон")
        try:
            phone = self.get_coder().decrypt(phone)
        except Exception as e:
            print(e)

        user = get_object_or_404(User, phone_number=phone)

        if user:
            user.regenerate_passcode()
            user_founded = True
        else:
            user = User.objects.create(phone_number=phone, first_name='Имя', last_name='Фамилия', patronymic='Отчество')
            user.regenerate_passcode()
            user_founded = False
        err = ""
        # except Exception as e:
        #    err = str(e)
        #   user_founded = False
        #   success = False

        self.data = {
            'err': err,
            'user_founded': user_founded,
            # 'success': success,
        }


class InitAuthenticationKeyAPI(APIViewBase):
    def on_get(self):
        phone = self.query_params.get('phone', '')
        passcode = self.query_params.get('passcode', -1)

        '''try:'''
        user = get_object_or_404(User, phone_number=phone)

        if user and user.compare_passcode(passcode):
            # token = user.regenerate_token()
            user.reset_passcode()
            private_key, public_key = generate_keys()

            self.request.session['private_key'] = private_key

            success = True
        else:
            # token = ''
            success = False

    '''except:
        self.request.session['private_key'] = public_key = ''
        success = False

    self.data = {
        'public_key': public_key,
        'success': success
    }'''


class AuthenticateUserAPI(APIViewBase):
    def on_get(self):
        key = self.query_params.get('key', '')

        '''try:'''
        data = self.decrypt(key)

        self.request.session['private_user_key'] = data

        success = True

    '''except:
        success = False

    self.data = {
        'success': success
    }'''


class UserInfoAPI(APIViewBase):
    def on_get(self):
        info = dict()

        # try:
        success = True
        user = user_by_token(self.query_params['token'])

        if not user:
            raise Exception()

        info['id'] = user.id
        info['first_name'] = user.first_name
        info['last_name'] = user.last_name
        info['patronymic'] = user.patronymic
        info['coins'] = user.coins

    '''except:
        success = False

    self.data = {
        'info': info,
        'success': success
    }'''


class UserGarbageInfoAPI(APIViewBase):
    def on_get(self):
        info = dict()

        # try:
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


'''except:
     success = False

 self.data = {
     'info': info,
     'success': success
 }'''
