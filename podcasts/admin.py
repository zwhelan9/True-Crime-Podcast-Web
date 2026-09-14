from django.contrib import admin
from .models import Podcast, Episode, Category, Review

admin.site.register(Podcast)
admin.site.register(Episode)
admin.site.register(Category)
admin.site.register(Review)