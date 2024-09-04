from django.contrib import admin
from .models import Service,Subscription


# Register your models here.
admin.site.register(Service)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'payment_terms')

admin.site.register(Subscription)