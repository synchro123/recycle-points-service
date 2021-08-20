from django.shortcuts import get_object_or_404
from .models import User, user_by_token
from .views import APIViewBase

from rest_framework.views import APIView
from rest_framework.response import Response


class UserAddGarbageAPIBase(APIViewBase):
    def on_get(self):
        try:
            success = True

            token = self.query_params['token']
            value = int(self.query_params['value'])

            user = user_by_token(token)

            if user:
                self.operate(user, value)
                user.coins += value
                user.save()
            else:
                success = False
        except:
            success = False

        self.data = {
            'success': success
        }

    def operate(self, user, value):
        pass


class UserAddCardboardAPI(UserAddGarbageAPIBase):
    def operate(self, user, value):
        user.garb_cardboard += value


class UserAddWastepaperAPI(UserAddGarbageAPIBase):
    def operate(self, user, value):
        user.garb_wastepaper += value


class UserAddGlassAPI(UserAddGarbageAPIBase):
    def operate(self, user, value):
        user.garb_glass += value


class UserAddPlasticLidAPI(UserAddGarbageAPIBase):
    def operate(self, user, value):
        user.garb_plastic_lid += value


class UserAddAluminumCanAPI(UserAddGarbageAPIBase):
    def operate(self, user, value):
        user.garb_aluminum_can += value


class UserAddPlasticBottleAPI(UserAddGarbageAPIBase):
    def operate(self, user, value):
        user.garb_plastic_bottle += value


class UserAddPlasticMk2API(UserAddGarbageAPIBase):
    def operate(self, user, value):
        user.garb_plastic_mk2 += value


class UserAddPlasticMk5API(UserAddGarbageAPIBase):
    def operate(self, user, value):
        user.garb_plastic_mk5 += value


class UserAddCoinsAPI(APIViewBase):
    def on_get(self):
        try:
            success = True

            token = self.query_params['token']
            value = int(self.query_params['value'])

            user = user_by_token(token)

            if user:
                user.coins += value
                user.save()
            else:
                success = False
        except:
            success = False

        self.data = {
            'success': success
        }
