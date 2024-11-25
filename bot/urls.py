from django.urls import path
from .views import bot_webhook

urlpatterns = [
    path("telegram/", bot_webhook, name="bot_webhook"),
]
