from django.contrib import admin

from news.models import Category, News


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

admin.site.register(Category, CategoryAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['category']

admin.site.register(News, NewsAdmin)
