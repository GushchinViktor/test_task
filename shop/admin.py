from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')  # Поля, которые будут отображаться в списке
    search_fields = ('name',)  # Возможность поиска по названию товара
    list_filter = ('price',)  # Фильтрация по цене


