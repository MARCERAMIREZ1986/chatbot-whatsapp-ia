from groq import Groq
from django.conf import settings
from ..models import Cliente, Conversacion, Mensaje,Agente
 # Configuramos la clave de OpenAI que ya tienes en .env
cliente_groq=Groq(api_key=settings.GROQ_API_KEY)


def obtener_o_crear_cliente(numero, nombre=""):
     """Busca al cliente por teléfono o lo registra si es nuevo"""
     cliente, _ = Cliente.objects.get_or_create(
         numero_telefono=numero,
         defaults={"nombre": nombre}
     )
     return cliente
def obtener_o_crear_conversacion(cliente, cuenta):
     """Busca conversación activa o crea una nueva"""
     conversacion = Conversacion.objects.filter(
         cliente=cliente,
         cuenta=cuenta,
         estado__in=["activa", "pendiente_agente"]
     ).first()
     if not conversacion:
         conversacion = Conversacion.objects.create(
             cliente=cliente,
             cuenta=cuenta
         )
     return conversacion
def generar_respuesta_ia(conversacion, mensaje_nuevo):
     print(f"mensaje: {mensaje_nuevo}")
     
     # 1. Si ya está pendiente de agente → no llamamos a la IA, solo avisamos
     if conversacion.estado == "pendiente_agente":
         return "✅ Un agente se pondrá en contacto contigo pronto."
     
     # 2. Si está activa → la IA responde normalmente
     historial = conversacion.mensaje.order_by("fecha_envio")[:10]
     
     mensajes_para_ia = [
         {"role": "system", "content": "Eres un asistente amable y eficiente. Responde de forma clara y breve."}
     ]
     
     for msg in historial:
         rol = "user" if msg.origen == "cliente" else "assistant"
         mensajes_para_ia.append({"role": rol, "content": msg.texto})
     
     mensajes_para_ia.append({"role": "user", "content": mensaje_nuevo})
     
     respuesta = cliente_groq.chat.completions.create(
         model="openai/gpt-oss-20b",
         messages=mensajes_para_ia,
         temperature=0.7
     )
     
     texto_respuesta = respuesta.choices[0].message.content.strip()
     print(f"Respuesta IA: {texto_respuesta}")
     
     # 3. Detectamos si el usuario pide hablar con alguien
     palabras_clave = ["hablar con alguien", "agente", "persona humana", "atención personalizada"]
     hay_palabra_clave = any(palabra in mensaje_nuevo.lower() for palabra in palabras_clave)
     
     if hay_palabra_clave:
         conversacion.estado = "pendiente_agente"
         
         # Asignar agente automáticamente
         try:
             agente = Agente.objects.get(nombre="Marcelo")
             conversacion.asignada_a = agente
         except Agente.DoesNotExist:
             print(" No se encontró el agente")
         print(f"cliente:{mensaje_nuevo}")
         conversacion.save()
         return " Entendido. En breve uno de nuestros agentes se pondrá en contacto contigo."
     
     return texto_respuesta