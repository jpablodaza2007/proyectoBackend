from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import auth, firestore
from biblioteca.firebase_config import initialize_firebase
import requests
import os
from functools import wraps

db = initialize_firebase()

# =========================
# REGISTRO DE USUARIO
# =========================
def registro_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Crear usuario en Firebase Auth
            user = auth.create_user(
                email=email,
                password=password
            )

            # Crear perfil en Firestore
            db.collection('perfiles').document(user.uid).set({
                'email': email,
                'uid': user.uid,
                'rol': 'usuario',
                'fecha_registro': firestore.SERVER_TIMESTAMP
            })

            messages.success(request, "✅ Usuario registrado correctamente.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"❌ Error en el registro: {e}")

    return render(request, 'registro.html')


# =========================
# INICIO DE SESIÓN
# =========================
def iniciar_sesion(request):

    if 'uid' in request.session:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        api_key = os.getenv('FIREBASE_WEB_API_KEY')

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }

        try:
            response = requests.post(url, json=payload)
            data = response.json()

            if response.status_code == 200:
                # Guardar sesión
                request.session['uid'] = data['localId']
                request.session['email'] = data['email']
                request.session['idToken'] = data['idToken']

                messages.success(request, "✅ Bienvenido a la Biblioteca")
                return redirect('dashboard')

            else:
                error = data.get('error', {}).get('message', 'ERROR')
                errores = {
                    'EMAIL_NOT_FOUND': 'Correo no registrado.',
                    'INVALID_PASSWORD': 'Contraseña incorrecta.',
                    'USER_DISABLED': 'Usuario deshabilitado.'
                }
                messages.error(request, errores.get(error, "Error de autenticación"))

        except Exception as e:
            messages.error(request, f"❌ Error al iniciar sesión: {e}")

    return render(request, 'login.html')


# =========================
# CERRAR SESIÓN
# =========================
def cerrar_sesion(request):
    request.session.flush()
    messages.info(request, "🔒 Sesión cerrada correctamente.")
    return redirect('login')


# =========================
# DECORADOR DE SEGURIDAD
# =========================
def login_required_firebase(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'uid' not in request.session:
            messages.warning(request, "Debes iniciar sesión.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# =========================
# DASHBOARD (ENTRADA A LA APP)
# =========================
@login_required_firebase
def dashboard(request):
    uid = request.session.get('uid')

    perfil = {}
    try:
        doc = db.collection('perfiles').document(uid).get()
        if doc.exists:
            perfil = doc.to_dict()
    except Exception as e:
        messages.error(request, f"Error cargando perfil: {e}")

    return render(request, 'dashboard.html', {'perfil': perfil})

# =========================
# DECORADOR DE SEGURIDAD
# =========================
def login_required_firebase(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'uid' not in request.session:
            messages.warning(request, "Acceso denegado. Inicia sesión.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# =========================
# LISTAR LIBROS
# =========================
@login_required_firebase
def listar_libros(request):
    uid = request.session.get('uid')
    libros = []

    try:
        docs = db.collection('libros').where('usuario_uid', '==', uid).stream()
        for doc in docs:
            libro = doc.to_dict()
            libro['id'] = doc.id
            libros.append(libro)
    except Exception as e:
        messages.error(request, f"Error al cargar libros: {e}")

    return render(request, 'biblioteca/listar.html', {'libros': libros})


# =========================
# CREAR LIBRO
# =========================
@login_required_firebase
def crear_libro(request):
    if request.method == 'POST':
        uid = request.session.get('uid')

        try:
            db.collection('libros').add({
                'titulo': request.POST.get('titulo'),
                'autor': request.POST.get('autor'),
                'anio': int(request.POST.get('anio')),
                'estado': 'Disponible',
                'usuario_uid': uid,
                'fecha_creacion': firestore.SERVER_TIMESTAMP
            })
            messages.success(request, "📘 Libro creado correctamente.")
            return redirect('listar_libros')
        except Exception as e:
            messages.error(request, f"Error al crear libro: {e}")

    return render(request, 'biblioteca/form.html')


# =========================
# EDITAR LIBRO
# =========================
@login_required_firebase
def editar_libro(request, libro_id):
    uid = request.session.get('uid')
    libro_ref = db.collection('libros').document(libro_id)

    try:
        doc = libro_ref.get()
        if not doc.exists:
            messages.error(request, "El libro no existe.")
            return redirect('listar_libros')

        libro = doc.to_dict()

        if libro.get('usuario_uid') != uid:
            messages.error(request, "No tienes permiso para editar este libro.")
            return redirect('listar_libros')

        if request.method == 'POST':
            libro_ref.update({
                'titulo': request.POST.get('titulo'),
                'autor': request.POST.get('autor'),
                'anio': int(request.POST.get('anio')),
                'estado': request.POST.get('estado'),
                'fecha_actualizacion': firestore.SERVER_TIMESTAMP
            })
            messages.success(request, "✏️ Libro actualizado.")
            return redirect('listar_libros')

    except Exception as e:
        messages.error(request, f"Error al editar libro: {e}")
        return redirect('listar_libros')

    return render(request, 'biblioteca/editar.html', {'libro': libro, 'id': libro_id})


# =========================
# ELIMINAR LIBRO
# =========================
@login_required_firebase
def eliminar_libro(request, libro_id):
    try:
        db.collection('libros').document(libro_id).delete()
        messages.success(request, "🗑️ Libro eliminado.")
    except Exception as e:
        messages.error(request, f"Error al eliminar libro: {e}")

    return redirect('listar_libros')
