# 📌 Expediente Electrónico

## 📖 Descripción
Expediente Electrónico es una aplicación diseñada para gestionar información de alumnos, asociaciones y gráficos de manera eficiente. Utiliza **NiceGUI** para proporcionar una interfaz de usuario moderna y amigable, junto con herramientas de visualización de datos como **Highcharts**.

## 🚀 Características
- 📂 **Gestión de Alumnos**: Registro, edición, importacion y manejo de alumnos con datos clave.
- 🏫 **Administración de Asociaciones**: Creación de asociaciones, gestión de miembros y archivos.
- 📊 **Visualización de Datos**: Carga y análisis de archivos Excel con gráficos interactivos.
- 📁 **Manejo de Archivos**: Subida y eliminación de archivos relacionados con alumnos y asociaciones.
- 🎨 **Interfaz Intuitiva**: UI moderna y dinámica con NiceGUI.

## 🛠️ Instalación
### 1️⃣ Requisitos Previos
- **Python 3.10+**
- **Virtualenv (Opcional pero recomendado)**

### 2️⃣ Clonar el Repositorio
```sh
git clone https://github.com/tu-usuario/expediente-electronico.git
cd expediente-electronico
```

### 3️⃣ Crear un Entorno Virtual (Opcional)
```sh
python -m venv env
source env/bin/activate  # En Linux/macOS
env\Scripts\activate  # En Windows
```

### 4️⃣ Instalar Dependencias
```sh
pip install -r requirements.txt
```

## ▶️ Uso
Para ejecutar la aplicación:
```sh
python main.py
```
La aplicación se ejecutará en `http://localhost:8000`

## 📦 Generar un Ejecutable (Windows)
Si deseas empaquetar la aplicación en un `.exe`, usa **PyInstaller**:
```sh
pyinstaller main.spec
```
Si **Highcharts no carga correctamente**, modifica `main.spec` para incluir archivos `.js` y `.css`.

## ⚙️ Estructura del Proyecto
```
expediente-electronico/
│-- static/          # Archivos estáticos (favicon, CSS, etc.)
│-- pages/           # Páginas de la aplicación (alumnos, asociaciones, gráficos)
│-- models/          # Modelos SQLAlchemy para la base de datos
│-- utils/           # Funciones auxiliares (carga de archivos, gráficos, etc.)
│-- database.py      # Configuración de la base de datos SQLite
│-- main.py          # Punto de entrada de la aplicación
│-- requirements.txt # Dependencias del proyecto
```


## 🏗️ Tecnologías Utilizadas
- **NiceGUI** → UI moderna y personalizable
- **SQLAlchemy** → Base de datos SQLite
- **Highcharts** → Visualización de datos interactiva
- **PyInstaller** → Empaquetado en ejecutable

## 📜 Licencia
MIT License © 2024 - Expediente Electrónico


---
_¡Gracias por usar Expediente Electrónico! 🚀_