# 📚 Sistema de Gestión de Biblioteca con Django + Firebase

Aplicación web desarrollada con **Django** integrada con **Firebase** como Backend as a Service (BaaS).

---

## 📝 Descripción

El sistema permite:

- Registro e inicio de sesión con Firebase Authentication
- Gestión de perfil de usuario en Firestore
- CRUD completo de libros
- Control de acceso por usuario (multiusuario)
- Seguridad basada en UID

---

## 🏗️ Arquitectura del Sistema

### 🔹 Backend
- Templates HTML
- Manejo de sesiones
- Decoradores personalizados de seguridad

### 🔹 Autenticación
- Registro → Firebase Admin SDK
- Inicio de sesión → Firebase REST API (identitytoolkit)
- Sesión almacenada en Django (uid, email, idToken)

### 🔹 Base de Datos
- Firestore (NoSQL)
- SQLite solo para uso interno de Django (admin, sesiones)

---

## 📂 Estructura del Proyecto

<pre>
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
</pre>


## proyectoBackend como carpeta principal

--

biblioteca como carpeta de proyecto

--

usuarios como carpeta de aplicación

--

requeriments como archivo de librerias

---

## 📊 Modelo de Datos (Firestore)

### Colección: perfiles
<pre><code class="json">
{
  "email": "usuario@email.com",
  "uid": "UID_GENERADO",
  "rol": "usuario",
  "fecha_registro": "timestamp"
}
</code></pre>

### Colección: libros
<pre><code class="json">
{
  "titulo": "Cien Años de Soledad",
  "autor": "Gabriel García Márquez",
  "anio": 1967,
  "estado": "Disponible",
  "usuario_uid": "UID_DEL_USUARIO",
  "fecha_creacion": "timestamp",
  "fecha_actualizacion": "timestamp"
}
</code></pre>

---

## 🔐 Seguridad Implementada

- Decorador personalizado `login_required_firebase`
- Validación de propietario antes de editar libro
- UID asociado a cada libro
- Variables de entorno para claves sensibles
- SDK inicializado dinámicamente con ruta absoluta

---

## 🚀 Instalación y Configuración

### 1️⃣ Clonar el repositorio
<pre><code class="bash">
git clone https://github.com/jpablodaza2007/proyectoBackend.git
cd proyectoBackend
</code></pre>

### 2️⃣ Crear entorno virtual

**Windows:**
<pre><code class="bash">
python -m venv venv
venv\Scripts\activate
</code></pre>

**Linux / Mac:**
<pre><code class="bash">
python3 -m venv venv
source venv/bin/activate
</code></pre>

### 3️⃣ Instalar dependencias
<pre><code class="bash">
pip install -r requirements.txt
</code></pre>

### 4️⃣ Configuración de Firebase
<pre>
1. Crear proyecto en la consola de Firebase
2. Habilitar Authentication (Email/Password) y Firestore Database
3. Descargar credenciales:
   - Project Settings → Service Accounts → Generate new private key
   - Guardar archivo JSON en biblioteca/serviceAccountKey.json
</pre>

### 5️⃣ Ejecutar migraciones
<pre><code class="bash">
python manage.py migrate
</code></pre>

### 6️⃣ Ejecutar servidor
<pre><code class="bash">
python manage.py runserver
</code></pre>

Abrir en navegador: `http://127.0.0.1:8000/`

---

## 📌 Endpoints Principales

### Autenticación

| Ruta           | Descripción      |
|----------------|----------------|
| `/`            | Login           |
| `/login/`      | Login           |
| `/registro/`   | Registro        |
| `/logout/`     | Cerrar sesión   |
| `/dashboard/`  | Panel de usuario|

### Biblioteca

| Ruta                            | Descripción     |
|---------------------------------|----------------|
| `/biblioteca/`                  | Listar libros   |
| `/biblioteca/crear/`            | Crear libro     |
| `/biblioteca/editar/<libro_id>/`   | Editar libro   |
| `/biblioteca/eliminar/<libro_id>/` | Eliminar libro |

---

## 🛠️ Dependencias Principales

<pre><code class="text">
Django
firebase-admin
python-dotenv
requests
</code></pre>

---

## ⚠️ Configuración para Producción

- Mover `SECRET_KEY` a variable de entorno
- Establecer `DEBUG=False`
- Configurar `ALLOWED_HOSTS`
- Usar base de datos robusta (PostgreSQL)
- Configurar reglas de seguridad en Firestore

---

## 👨‍💻 Autor y Colaboradores

**Autor:** Juan Pablo Daza Alcazar

**Colaboradores:**
- Joseph Sebastian Cristiano Beltran
- Jhostyn Nicolas Cristiano Beltran
- Juan Manuel Baracaldo

Programa ADSO – Análisis y Desarrollo de Software

---

## 🎯 Características Técnicas Destacadas

✔ Integración real Django + Firebase  
✔ Autenticación híbrida (Admin SDK + REST API)  
✔ Multiusuario con separación por UID  
✔ Arquitectura cliente-servidor  
✔ Control de acceso personalizado  
✔ Modelo NoSQL documentado
