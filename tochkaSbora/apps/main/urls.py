from django.urls import path
from . import views
from .add_garbage_views import *

urlpatterns = [
    path('api/create_user', views.CreateUserAPI.as_view(), name='createUserAPI'),

    path('api/try_authentication', views.TryAuthenticationAPI.as_view(), name='tryAuthenticationUserAPI'),
    path('api/init_authentication', views.InitAuthenticationAPI.as_view(), name='initAuthenticationUserAPI'),
    path('api/authenticate_user', views.AuthenticateUserAPI.as_view(), name='authenticateUserAPI'),

    path('api/get_user_qr_token', views.GetUserQRTokenAPI.as_view(), name='getUserQRTokenAPI'),

    path('api/user_info', views.UserInfoAPI.as_view(), name='userInfoAPI'),
    path('api/user_garbage_info', views.UserGarbageInfoAPI.as_view(), name='userGarbageInfoAPI'),

    path('api/add_garbage/cardboard', UserAddCardboardAPI.as_view(), name='addCardboardUserAPI'),
    path('api/add_garbage/wastepaper', UserAddWastepaperAPI.as_view(), name='addAddWastepaperUserAPI'),
    path('api/add_garbage/glass', UserAddGlassAPI.as_view(), name='addGlassAPIUserAPI'),
    path('api/add_garbage/plastic_lid', UserAddPlasticLidAPI.as_view(), name='addPlasticLidUserAPI'),
    path('api/add_garbage/aluminium_can', UserAddAluminumCanAPI.as_view(), name='addAluminumCanUserAPI'),
    path('api/add_garbage/plastic_bottle', UserAddPlasticBottleAPI.as_view(), name='addPlasticBottleUserAPI'),
    path('api/add_garbage/plastic_mk2', UserAddPlasticMk2API.as_view(), name='addPlasticMk2UserAPI'),
    path('api/add_garbage/plastic_mk5', UserAddPlasticMk5API.as_view(), name='addPlasticMk5UserAPI'),
    path('api/add_coins', UserAddCoinsAPI.as_view(), name='addCoinsUserAPI'),

    path('api/collection_places_list', views.CollectionPlacesInfoAPI.as_view(), name='collectionPlacesInfoAPI'),
    path('api/markets_list', views.MarketsInfoAPI.as_view(), name='marketsInfoAPI'),
    path('api/market_items_list', views.MarketItemsInfoAPI.as_view(), name='marketItemsInfoAPI'),
    path('api/market_item_info', views.MarketItemInfoAPI.as_view(), name='marketItemInfoAPI'),
]