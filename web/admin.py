from django.contrib import admin

from .models import *


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_id', 'name', 'ip_addr', 'is_active', 'created_at', 'modified_at')
    list_filter = ('is_active', 'created_at',)
    ordering = ('id',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'index', 'room', 'name', 'user_id', 'ip_addr', 'is_active', 'created_at', 'modified_at')
    list_filter = ('room', 'is_active', 'created_at',)
    ordering = ('id',)


admin.site.register(Room, RoomAdmin)
admin.site.register(Post, PostAdmin)
