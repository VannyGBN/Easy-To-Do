from django.urls import path
from .views import home, crear_cuenta

urlpatterns = [
    path('', home, name='home'),
    path('crear-cuenta/', crear_cuenta, name='crear_cuenta'),
]