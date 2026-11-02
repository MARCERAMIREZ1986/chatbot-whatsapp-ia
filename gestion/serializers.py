from rest_framework import serializers
from .models import CuentaWhatsapp, Cliente, Conversacion, Mensaje

class CuentaWhatsappSerializers(serializers.ModelSerializer):
    class Meta:
        model = CuentaWhatsapp
        field = ["id","nombre","proveedor","numero_telefono","activa","fecha_creacion"]
        read_only_fields = ["fecha_creacion"]

class ClienteSerealizers(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"

class MensajeSerealizers(serializers.ModelSerializer):
    origen_nombre = serializers.CharField(source="get_origen_display", read_only=True)
    class Meta:
        model = Mensaje
        fields = ["id","origen","origen_nombre","texto","fecha_envio","leido"]
        read_only_fields = ["fecha_envio"]

class ConversacionDetalleSerializers(serializers.ModelSerializer):
    cliente = ClienteSerealizers(read_only=True)
    mensaje = MensajeSerealizers(many=True, read_only=True)
    ultimo_mensaje = serializers.DateTimeField(source="mensajes_fecha_envio", read_only=True)
    class Meta:
        model =  Conversacion
        fields = ["id", "cliente","estado","asignada_a","fecha_inicio","mensaje","ultimo_mensaje"]
