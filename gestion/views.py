from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action 
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CuentaWhatsapp, Cliente, Conversacion, Mensaje
from .serializers import(
    CuentaWhatsappSerializers, ClienteSerealizers, ConversacionDetalleSerializers, MensajeSerealizers
)
from twilio.rest import Client
from django.conf import settings
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt
from .servicios.procesador import (
     obtener_o_crear_cliente,
     obtener_o_crear_conversacion,
     generar_respuesta_ia,
 )
class CuentaWhatsappViewSet(viewsets.ReadOnlyModelViewSet):
    #para usuarios autorizados
    serializer_class = CuentaWhatsappSerializers
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return CuentaWhatsapp.objects.filter(activa=True)
    
class ConversacionViewSet(viewsets.ReadOnlyModelViewSet):
    #lista y ve detalles las conversaicones
    serializers_class = ConversacionDetalleSerializers
    permission_classes = [IsAuthenticated]
    def  get_queryset(self):
        return Conversacion.objects.select_related("cliente","asignada_a").prefetch_related("mensaje")
    @action (detail=True, methods=["post"])
    def asignar_agente(self, request, pk=None):
        #accion para pasar conversacion a un agente
        conversacion = self.get_object()
        agente_id = request.data.get("agente_id")
        if not agente_id:
            return Response({"error":"Falta el ID del agente"},status=status.HTTP_400_BAD_REQUEST)
        
        conversacion.asignada_a_id = agente_id
        conversacion_estado = "pendiente_agente"
        conversacion.save()
        return Response({"mensaje","Conversacion asignada correctamente"})



 # Inicializamos Twilio
cliente_twilio = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
@csrf_exempt  # Necesario porque Twilio no envía el token CSRF
def webhook_whatsapp(request):
     print("llego")
     print("Metodo",request.method)
     """Recibe mensajes desde WhatsApp y devuelve la respuesta"""
     if request.method != "POST":
         return HttpResponse("Método no permitido", status=405)
     # Extraemos los datos que envía Twilio
     numero_remitente = request.POST.get("From", "").replace("whatsapp:", "")
     numero_destino = request.POST.get("To", "").replace("whatsapp:", "")
     texto_mensaje = request.POST.get("Body", "").strip()
     # Buscamos la cuenta asociada a ese número
     try:
         #cuenta = CuentaWhatsapp.objects.get(numero_telefono=numero_destino, activa=True)
         cuenta = CuentaWhatsapp.objects.get(numero_telefono=numero_remitente)
     except CuentaWhatsapp.DoesNotExist:
         return HttpResponse("Cuenta no configurada", status=404)
     # Procesamos cliente y conversación
     cliente = obtener_o_crear_cliente(numero_remitente)
     conversacion = obtener_o_crear_conversacion(cliente, cuenta)
     # Guardamos el mensaje del cliente
     Mensaje.objects.create(
         conversacion=conversacion,
         origen="cliente",
         texto=texto_mensaje
     )
     # Generamos respuesta
   
     respuesta = generar_respuesta_ia(conversacion, texto_mensaje)
     # Guardamos la respuesta del sistema
     Mensaje.objects.create(
         conversacion=conversacion,
         origen="bot",
         texto=respuesta
     )
     # Enviamos la respuesta por WhatsApp
     cliente_twilio.messages.create(
         body=respuesta,
         from_=f"whatsapp:{numero_destino}",
         to=f"whatsapp:{numero_remitente}"
     )
    

 #  Te avisás a VOS mismo
     if "En breve uno de nuestros agentes" in respuesta:
           from gestion.models import Agente
           try:
               agente = Agente.objects.get(nombre="Marcelo")
               if agente.telefono:
                   numero_texto = str(agente.telefono).strip()
                   tu_numero = f"whatsapp:{numero_texto}" # ← CAMBIÁ por TU número
                   print(f"numero limpio : {numero_texto}")
                   cliente_twilio.messages.create(
                   body=f" NECESITAN AGENTE\nCliente: {numero_remitente}",
                   from_=f"whatsapp:{numero_destino}",
                   to=tu_numero
                   )
           except Agente.DoesNotExist:
               print("no se encontro al agente")
     return HttpResponse("Mensaje procesado correctamente")
     
 
 


@action(detail=True, methods=["post"])
def asignar_agente(self, request, pk=None):
     conversacion = self.get_object()
     agente_id = request.data.get("agente_id")
     
     if not agente_id:
         return Response({"error": "Falta el ID del agente"}, status=400)
     
     # Asignamos el agente
     conversacion.asignada_a_id = agente_id
     
     #  Cambiamos el estado de vuelta a activa
     conversacion.estado = "activa"
     conversacion.save()
     
     return Response({"mensaje": " Agente asignado correctamente"})