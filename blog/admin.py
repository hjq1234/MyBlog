from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Tag, Post


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'is_draft', 'created_at', 'updated_at')
    list_filter = ('is_draft', 'tags')
    search_fields = ('title',)
    filter_horizontal = ('tags',)
    list_editable = ('is_draft',)

    class Media:
        css = {'all': ('blog/css/admin_custom.css',)}
