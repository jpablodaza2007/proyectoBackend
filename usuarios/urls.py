from django.urls import path
from django.shortcuts import redirect
from .views import (
    registro_usuario,
    iniciar_sesion,
    cerrar_sesion,
    dashboard,
    listar_libros,
    crear_libro,
    editar_libro,
    eliminar_libro
)

urlpatterns = [
    path('', iniciar_sesion, name='inicio'),
    path('registro/', registro_usuario, name='registro'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('biblioteca/', listar_libros, name='listar_libros'),
    path('biblioteca/crear/', crear_libro, name='crear_libro'),
    path('biblioteca/editar/<str:libro_id>/', editar_libro, name='editar_libro'),
    path('biblioteca/eliminar/<str:libro_id>/', eliminar_libro, name='eliminar_libro'),
]
