# coding: utf-8
from django.contrib import admin

from onadata.apps.logger.models import XForm, Instance


class FormAdmin(admin.ModelAdmin):

    exclude = ('user',)
    list_display = ('id_string', 'description', 'user', 'allow_auth_submit', 'downloadable', 'shared')

    # A user should only see forms that belong to him.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

class FormInstance(admin.ModelAdmin):
    list_display = ('pk', 'user', 'xform')

admin.site.register(XForm, FormAdmin)
admin.site.register(Instance, FormInstance)
