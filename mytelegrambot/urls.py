from django.contrib import admin
from django.urls import path, include  # Импортируйте include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bot/', include('bot.urls')),  # Включите маршруты вашего приложения
]