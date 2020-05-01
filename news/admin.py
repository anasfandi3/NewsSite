from django.contrib import admin

from news.models import Category, News, Images

class NewsImageInline(admin.TabularInline):
    model = Images
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['category']
    inlines = [NewsImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'news', 'image']


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Images, ImagesAdmin)
