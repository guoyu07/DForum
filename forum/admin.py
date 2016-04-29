from django.contrib import admin
from models import User,Node,Topic,Plane

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'nickname')
    list_filter = ('is_active', 'is_staff', 'date_joined')


@admin.register(Plane)
class PlaneAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    search_fields = ('name',)
    list_filter = ('created',)

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created')
    search_fields = ('name',)
    list_filter = ('created',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    search_fields = ('title', 'content')
    list_filter = ('created',)