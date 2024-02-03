from django.contrib import admin

from social_content.models import Content, Author


# Register your models here.
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass
