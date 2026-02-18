📘 README.md — Sistema de Gestión de Biblioteca con Django + Firebase
📚 Sistema de Gestión de Biblioteca

Aplicación web desarrollada con Django integrada con Firebase como Backend as a Service (BaaS).

El sistema permite:

Registro e inicio de sesión con Firebase Authentication

Gestión de perfil de usuario en Firestore

CRUD completo de libros

Control de acceso por usuario (multiusuario)

Seguridad basada en UID

🏗️ Arquitectura del Sistema
🔹 Backend

Templates HTML

Manejo de sesiones

Decoradores personalizados de seguridad

🔹 Autenticación

Registro → Firebase Admin SDK

Inicio de sesión → Firebase REST API (identitytoolkit)

Sesión almacenada en Django (uid, email, idToken)

🔹 Base de Datos

Firestore (NoSQL)

SQLite solo para uso interno de Django (admin, sesiones)

📂 Estructura del Proyecto
proyectoBackend/
│
├── biblioteca/
│   ├── settings.py
│   ├── urls.py
│   ├── firebase_config.py
│
├── usuarios/
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│
├── manage.py
├── requirements.txt
└── db.sqlite3

📊 Modelo de Datos (Firestore)
📁 Colección: perfiles
{
  "email": "usuario@email.com",
  "uid": "UID_GENERADO",
  "rol": "usuario",
  "fecha_registro": "timestamp"
}

📁 Colección: libros
{
  "titulo": "Cien Años de Soledad",
  "autor": "Gabriel García Márquez",
  "anio": 1967,
  "estado": "Disponible",
  "usuario_uid": "UID_DEL_USUARIO",
  "fecha_creacion": "timestamp",
  "fecha_actualizacion": "timestamp"
}

🔐 Seguridad Implementada

Decorador personalizado login_required_firebase

Validación de propietario antes de editar libro

UID asociado a cada libro

Variables de entorno para claves sensibles

SDK inicializado dinámicamente con ruta absoluta

🚀 Instalación y Configuración
1️⃣ Clonar el repositorio
git clone https://github.com/jpablodaza2007/proyectoBackend.git
cd proyectoBackend

2️⃣ Crear entorno virtual
Windows:
python -m venv venv
venv\Scripts\activate

Linux / Mac:
python3 -m venv venv
source venv/bin/activate

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Configuración de Firebase
🔹 Paso 1: Crear proyecto en Firebase

Entra a la consola de Firebase
Crea un proyecto nuevo.

🔹 Paso 2: Habilitar:

Authentication (Email/Password)

Firestore Database

🔹 Paso 3: Descargar credenciales

Ir a:
Project Settings → Service Accounts → Generate new private key

Guardar el archivo JSON dentro de la carpeta biblioteca/

Ejemplo:

biblioteca/serviceAccountKey.json

5️⃣ Ejecutar migraciones
python manage.py migrate

6️⃣ Ejecutar servidor
python manage.py runserver


Abrir en navegador:

http://127.0.0.1:8000/

📌 Endpoints Principales
🔐 Autenticación

/ → Login

/login/

/registro/

/logout/

/dashboard/

📚 Biblioteca

/biblioteca/

/biblioteca/crear/

/biblioteca/editar/<libro_id>/

/biblioteca/eliminar/<libro_id>/

🛠️ Dependencias Principales

Django

firebase-admin

python-dotenv

requests

⚠️ Configuración para Producción

Se recomienda:

Mover SECRET_KEY a variable de entorno

Establecer DEBUG=False

Configurar ALLOWED_HOSTS

Usar base de datos robusta (PostgreSQL)

Configurar reglas de seguridad en Firestore

👨‍💻 Autor

Juan Pablo Daza Alcazar

Colaboradores

Joseph Sebastian Cristiano Beltran
Jhostyn Nicolas Cristiano Beltran

Programa ADSO – Análisis y Desarrollo de Software

🎯 Características Técnicas Destacadas

✔ Integración real Django + Firebase
✔ Autenticación híbrida (Admin SDK + REST API)
✔ Multiusuario con separación por UID
✔ Arquitectura cliente-servidor
✔ Control de acceso personalizado
✔ Modelo NoSQL documentado
