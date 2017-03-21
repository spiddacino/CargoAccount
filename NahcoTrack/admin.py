from django.contrib import admin

from .models import Location,Software,Bank,AgencyDetail,AgentAWBList,Payments,PaymentUtilizations,TellerData,DailySales

# Register your models here.
admin.site.register(Location)
admin.site.register(Software)
admin.site.register(Bank)
admin.site.register(AgencyDetail)
admin.site.register(AgentAWBList)
admin.site.register(Payments)
admin.site.register(PaymentUtilizations)
admin.site.register(TellerData)
admin.site.register(DailySales)
