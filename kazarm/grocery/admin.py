from django.contrib import admin
from .models import *


admin.site.register(First_stage)
admin.site.register(Warehouse)
admin.site.register(Store)


@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    # list_filter = ('status', 'title', 'created', 'updated', 'warehouse')
    # search_fields = ('title', 'id', 'status', 'created', 'updated', 'warehouse')
    # ordering = ('status', 'publish')


@admin.register(Container)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'updated', 'warehouse', 'status')
    list_filter = ('status', 'title', 'created', 'updated', 'warehouse')
    search_fields = ['id', 'status', 'title__title']
    # ordering = ('status', 'publish')