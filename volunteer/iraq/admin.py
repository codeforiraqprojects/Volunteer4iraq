# Register your models here.
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import *
from iraq.models import CustomUser




class UserModel(UserAdmin):
    pass




admin.site.register(CustomUser,UserModel)
admin.site.register(Region)
admin.site.register(Gender)
admin.site.register(Classification)
admin.site.register(AdminHOD)
admin.site.register(People)
admin.site.register(Intity)
admin.site.register(Member)
admin.site.register(Poster)
admin.site.register(NumVolunteer)
admin.site.register(Comment)
admin.site.register(Comment_User)
admin.site.register(Reply)












