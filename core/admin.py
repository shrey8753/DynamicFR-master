from django.contrib import admin
from . import models
# Register your models here.


class LogsAdmin(admin.ModelAdmin):
    list_display = ('person', '', 'description', 'status')
    list_display_links = ('user', 'userprofile')
    list_filter = ('description', 'status')
    list_editable = ('description', 'status')
    search_fields = ('user', 'userprofile', 'description', 'status')
    list_max_show_all = 100



admin.site.register(models.Person)
admin.site.register(models.Station)
admin.site.register(models.Log)
