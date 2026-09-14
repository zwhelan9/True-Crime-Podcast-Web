from django.contrib import admin
from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'show_in_nav')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'content')