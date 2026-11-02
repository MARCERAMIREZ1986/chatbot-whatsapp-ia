from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CuentaWhatsappViewSet, ConversacionViewSet, webhook_whatsapp


router = DefaultRouter()
router.register(r"cuentas", CuentaWhatsappViewSet, basename="cuentas")
router.register(r"conversaciones", ConversacionViewSet, basename="conversaciones")

urlpatterns = [
    path("",include(router.urls)),
    path("webhook/whatsapp/",webhook_whatsapp, name="webhook_whatsapp"),
]
