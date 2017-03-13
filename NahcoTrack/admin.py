from django.contrib import admin

from .models import Location,Software,Bank,AgencyDetail

# Register your models here.
admin.site.register(Location)
admin.site.register(Software)
admin.site.register(Bank)
admin.site.register(AgencyDetail)
