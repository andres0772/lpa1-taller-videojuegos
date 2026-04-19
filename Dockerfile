# =============================================================================
# Dockerfile para LPA1 - Taller de Videojuegos
# Juego Python con Arcade + Pymunk (física 2D)
# =============================================================================

# Usar Python 3.12 slim - versión estable con amplia compatibilidad de paquetes
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# =============================================================================
# INSTALAR DEPENDENCIAS DEL SISTEMA
# =============================================================================
# Pymunk requiere compilación C (gcc) y librerías de gráficos para Arcade
# Las librerías mesa/libgl son necesarias para renderizado OpenGL en contenedor
# Librerías de fuentes/imágenes necesarias para pyglet (motor gráfico de Arcade)
RUN apt-get update && apt-get install -y --no-install-recommends \
gcc \
libgl1-mesa-dev \
libglib2.0-0 \
libsm6 \
libxext6 \
libxrender1 \
libfreetype6 \
fontconfig \
libjpeg62-turbo \
libpng-dev \
zlib1g-dev \
&& rm -rf /var/lib/apt/lists/*

# =============================================================================
# INSTALAR DEPENDENCIAS PYTHON
# =============================================================================
# Copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias con versiones fijas (reproducibilidad total)
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# COPIAR PROYECTO
# =============================================================================
COPY . .

# =============================================================================
# CONFIGURACIÓN POR DEFECTO
# =============================================================================
# El comando ejecuta el juego principal
CMD ["python", "main.py"]
