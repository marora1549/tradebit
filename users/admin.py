from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, UserSettings


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'profile_image')}),
    )


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'default_view')
    list_filter = ('theme', 'default_view')
    search_fields = ('user__username', 'user__email')
