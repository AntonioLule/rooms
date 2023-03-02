from django.contrib import admin

# Register your models here.
from apps.rent.models import TypeUser, EventsType

admin.site.register(TypeUser)
admin.site.register(EventsType)