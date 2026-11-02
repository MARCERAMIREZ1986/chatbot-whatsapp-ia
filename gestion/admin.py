from django.contrib import admin
from .models import CuentaWhatsapp, Cliente, Conversacion, Mensaje


admin.site.register(CuentaWhatsapp)
admin.site.register(Cliente)
admin.site.register(Conversacion)
admin.site.register(Mensaje)



# Register your models here.
