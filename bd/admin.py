from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Check)
admin.site.register(Order)
admin.site.register(Ticket)
admin.site.register(Delivery)
admin.site.register(Flight_Ticket)