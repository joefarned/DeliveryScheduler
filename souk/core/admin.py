from django.contrib import admin
from .models import Item, Nest, Profile, Request, CraigPost, Message

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Nest)
class NestAdmin(admin.ModelAdmin):
    pass

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(CraigPost)
class CraigPostAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
