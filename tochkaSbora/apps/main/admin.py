from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'patronymic', 'phone_number', 'passcode',
                    'garb_cardboard', 'garb_wastepaper', 'garb_glass', 'garb_plastic_lid',
                    'garb_aluminum_can', 'garb_plastic_bottle', 'garb_plastic_mk2', 'garb_plastic_mk5']

admin.site.register(User, UserAdmin)