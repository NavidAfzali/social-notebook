from django.contrib import admin
from .models import Note, Comment, Like


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'updated']
    search_fields = ['title', 'body']
    list_filter = ['updated']
    prepopulated_fields = {'slug': ['title']}
    raw_id_fields = ['user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'created', 'is_reply')
    raw_id_fields = ('user', 'note', 'reply')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('note', 'user')
