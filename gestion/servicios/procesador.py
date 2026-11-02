from groq import Groq
from django.conf import settings
from ..models import Cliente, Conversacion, Mensaje
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
     """Construye el historial y pide respuesta a la IA"""
     # Obtenemos los mensajes anteriores para dar contexto
     historial = conversacion.mensaje.order_by("fecha_envio")[:10]  # últimos 10 mensajes
     mensajes_para_ia = [
         {"role": "system", "content": """
             Eres un asistente amable y eficiente para una empresa.
             Responde de forma clara, breve y útil. Si no sabes algo, indícalo.
             Si el cliente pide hablar con una persona, avisa que lo derivarás.
         """}
     ]
     # Agregamos el historial
     for msg in historial:
         rol = "user" if msg.origen == "cliente" else "assistant"
         mensajes_para_ia.append({"role": rol, "content": msg.texto})
     # Agregamos el mensaje actual
     mensajes_para_ia.append({"role": "user", "content": mensaje_nuevo})
     # Llamamos a la IA
     
     respuesta = cliente_groq.chat.completions.create(
         model="openai/gpt-oss-120b",
         messages=mensajes_para_ia,
         temperature=0.7
     )
     texto_respuesta = respuesta.choices[0].message.content.strip()
     #  Detectamos si pide hablar con agente humano
     palabras_clave = ["hablar con alguien", "agente", "persona humana", "atención personalizada"]
     if any(palabra in texto_respuesta.lower() or palabra in mensaje_nuevo.lower() for palabra in palabras_clave):
         conversacion.estado = "pendiente_agente"
         conversacion.save()
         texto_respuesta = "Entendido. En breve uno de nuestros agentes se pondrá en contacto contigo. Quedo atento."
     return texto_respuesta
