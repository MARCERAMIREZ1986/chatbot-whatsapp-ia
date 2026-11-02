Un sistema de atención automática por WhatsApp construido con Django que integra modelos de lenguaje para responder consultas de forma inteligente.
 
 
 
 Descripción del Proyecto
 
Este proyecto permite crear un asistente virtual que funciona a través de WhatsApp. Recibe los mensajes de los usuarios, los procesa y devuelve respuestas generadas por inteligencia artificial. Es ideal para automatizar atención al cliente, respuestas frecuentes y mejorar la comunicación con usuarios.
 
 
 
 Tecnologías Utilizadas
 
- Python 3.x

- Django — Framework web

- Twilio API — Integración con WhatsApp

- Groq — Modelos de inteligencia artificial

- ngrok — Exposición local para pruebas
 
 
 
 Funcionalidades
 
-  Recibir mensajes desde WhatsApp

-  Generar respuestas automáticas con IA

-  Mantener el contexto de la conversación

-  Detectar palabras clave para derivar a un agente humano

-  Respuesta inmediata y personalizada
 
 
 
 Cómo funciona
 
1. El usuario envía un mensaje desde WhatsApp al número de Twilio

2. Twilio envía el mensaje a nuestro servidor mediante un webhook

3. Django recibe el mensaje y lo procesa

4. Se consulta al modelo de IA para generar una respuesta

5. La respuesta se envía de vuelta al usuario por WhatsApp