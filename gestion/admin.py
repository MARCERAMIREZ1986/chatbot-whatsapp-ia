from django.contrib import admin
from .models import CuentaWhatsapp, Cliente, Conversacion, Mensaje,Agente



admin.site.register(CuentaWhatsapp)
admin.site.register(Cliente)
admin.site.register(Conversacion)
admin.site.register(Mensaje)
admin.site.register(Agente)



# Register your models here.
