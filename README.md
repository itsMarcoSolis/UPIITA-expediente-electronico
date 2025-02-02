# UPIITA - Expediente Electrónico

## Descripción
Sistema de gestión local para el almacenamiento y administración de expedientes electrónicos de alumnos. Permite la carga de documentos, la gestión de asociaciones escolares y la visualización de gráficos relevantes.

## Características Principales
- Búsqueda de alumnos por número de boleta.
- Módulo para subir y administrar documentos PDF e imágenes.
- Registro y administración de asociaciones escolares.
- Creación de grupos dentro de las asociaciones.
- Visualización de datos a través de gráficos.

## Tecnologías Utilizadas
- **Backend:** Python con FastAPI
- **Frontend:** NiceGUI
- **Base de Datos:** SQLite
- **Autenticación:** JWT para gestión de usuarios
- **Almacenamiento de archivos:** Sistema de archivos local

## Instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/itsMarcoSolis/UPIITA-expediente-electronico.git
   cd UPIITA-expediente-electronico
   ```
2. Crear un entorno virtual e instalar dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Ejecutar la aplicación:
   ```bash
   python main.py
   ```

## Uso
- Acceder a la interfaz a través de `http://localhost:8000`
- Iniciar sesión con un usuario autorizado
- Gestionar expedientes y asociaciones desde el panel de control

## Seguridad
- Autenticación basada en JWT
- Restricción de acceso por roles
- Almacenamiento seguro de documentos

## Contacto
Para reportar errores o sugerencias, abre un issue en el repositorio o contacta con el equipo de desarrollo.

