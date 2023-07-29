from django.contrib import admin

from onadata.apps.main.models.user_profile import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'organization')


admin.site.register(UserProfile, UserProfileAdmin)