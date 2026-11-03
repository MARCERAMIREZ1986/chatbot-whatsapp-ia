from django.db import models
from django.contrib.auth.models import User

class CuentaWhatsapp(models.Model):
    OPCIONES_PROVEEDOR = [("twilio","Twilio/Meta API Oficial"),
                        ("otra","Otro provedor"),
                        ]
    nombre = models.CharField(max_length=100, verbose_name="NOMBRE DE LA CUENTA")
    proveedor = models.CharField(max_length=30, choices=OPCIONES_PROVEEDOR)
    numero_telefono = models.CharField(max_length=20, verbose_name="Numero con codigo pais")
    credenciales = models.JSONField(verbose_name="credenciales", help_text="Almacenamiento seguro de claves")
    activa = models.BooleanField(default=True, verbose_name="¿Activa?")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
         verbose_name = "Cuenta de WhatsApp"
         verbose_name_plural = "Cuentas de WhatsApp"
    def __str__(self):
         return f"{self.nombre}-{self.numero_telefono}"
class Cliente(models.Model):
     #datos de la persona que escribe al bot
     nombre = models.CharField(max_length=100, blank=True)
     numero_telefono = models.CharField(max_length=20, unique=True, verbose_name="Numero de telefono")
     ultimo_mensaje = models.DateTimeField(auto_now=True)
     class Meta:
          verbose_name = "Cliente"
          verbose_name_plural = "Clientes"
     def __str__(self):
          return self.nombre or self.numero_telefono
     

class Agente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    
    def __str__(self):
        return self.nombre
     
class Conversacion(models.Model):
     
     ESTADOS = [("activa","Activa"),("pendente_agente","Pasa a agente humano"),("cerrada","Finalizada")]
     cuenta = models.ForeignKey(CuentaWhatsapp, on_delete=models.CASCADE, related_name="conversaciones")
     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="chats")
     estado = models.CharField(max_length=25, choices=ESTADOS, default="activa")
     asignada_a = models.ForeignKey(Agente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Agente asignado")
     fecha_inicio = models.DateTimeField(auto_now_add=True)
     class Meta:
          verbose_name = "Conversacion"
          verbose_name_plural = "Conversaciones"
    
     def __str__(self):
        return f"{self.cliente}|{self.get_estado_display()}"
class Mensaje(models.Model):
     
     ORIGEN = [
          ("cliente","Enviado por cliente"),
          ("bot","Enviado por el asistente"),
          ("agente","Enviado por agente")
     ]
     
     conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name="mensaje")
     origen = models.CharField(max_length=15, choices=ORIGEN)
     texto = models.TextField(verbose_name="Contendido del mensaje")
     fecha_envio = models.DateTimeField(auto_now_add=True)
     leido = models.BooleanField(default=False)
     class Meta:
          ordering = ["fecha_envio"]# siempre ordenados del mas antiguo al nuevo 
          verbose_name = "Mensaje"
          verbose_name_plural = "Mensajes"
     def __str__(self):
       return f"{self.get_origen_display()}:{self.texto[:40]}..."
  
  


   