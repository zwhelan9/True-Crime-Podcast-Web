from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True)

    show_in_nav = models.BooleanField(default=True)

    def __str__(self):
        return self.title