from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import *



admin.site.register(Target)

from martor.widgets import AdminMartorWidget
class ReportAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

admin.site.register(Report, ReportAdmin)


class EntryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
admin.site.register(Entry, EntryAdmin)


class ProjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

admin.site.register(Project, ProjectAdmin)
admin.site.register(DomainCredentials)