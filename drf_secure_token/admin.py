from django.contrib import admin

from drf_secure_token.models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created', 'marked_for_delete')
    ordering = ('-created',)
    readonly_fields = ('key',)
