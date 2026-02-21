from django.contrib import admin
from .models import Category, Blog, About, SocialLink

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured')
    search_fields = ('id', 'title', 'category__category_name', 'status')
    list_editable = ('is_featured',)
    def has_add_permission(self, request):
        count = About.objects.all().count()
        return count == 0

class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at') 

admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(SocialLink)


 