"""Cargador de sprites desde spritesheet de Kenney."""

import arcade
from PIL import Image

from .sprites import (
    SPRITESHEET_CHARACTERS,
    SPRITESHEET_TILES,
    TILE_SIZE,
    MARGIN,
    TILE_STEP,
    JUGADOR,
    ENEMIGO_TERRESTRE,
    ENEMIGO_VOLADOR,
    JEFE,
    TESORO,
    PROYECTIL_JUGADOR,
    PROYECTIL_ENEMIGO,
)

# Cache global de texturas para evitar abrir el archivo repetidamente
_texturas_cache: dict[tuple[str, int, int], arcade.Texture] = {}


def cargar_sprite(config: dict, sheet_path: str) -> arcade.Sprite:
    """
    Carga un sprite desde el spritesheet.

    Args:
        config: Diccionario con 'row', 'col', 'scale'
        sheet_path: Ruta al spritesheet PNG

    Returns:
        arcade.Sprite configurado

    Raises:
        FileNotFoundError: Si el spritesheet no existe
        ValueError: Si las coordenadas exceden el tamaño de la imagen
    """
    sprite = arcade.Sprite()

    # Calcular posición en el spritesheet
    row = config["row"]
    col = config["col"]
    x = col * TILE_STEP
    y = row * TILE_STEP

    # Verificar cache primero
    cache_key = (sheet_path, row, col)
    if cache_key in _texturas_cache:
        sprite.texture = _texturas_cache[cache_key]
        sprite.scale = config.get("scale", 1.0)
        return sprite

    # Cargar la imagen completa con PIL (wrappeado en try/except)
    try:
        full_image = Image.open(sheet_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Error: No se encontró el spritesheet '{sheet_path}'. "
            "Verifica que el archivo existe en la ruta especificada."
        )
    except IOError as e:
        raise IOError(
            f"Error al abrir el spritesheet '{sheet_path}': {e}"
        )

    # Validar que las coordenadas no excedan el tamaño de la imagen
    if x + TILE_SIZE > full_image.width or y + TILE_SIZE > full_image.height:
        full_image.close()
        raise ValueError(
            f"Error: Las coordenadas (row={row}, col={col}) exceden el spritesheet. "
            f"El spritesheet mide {full_image.width}x{full_image.height} "
            f"y el sprite requiere posición ({x + TILE_SIZE}, {y + TILE_SIZE})."
        )

    # Recortar la región del sprite
    sprite_image = full_image.crop((x, y, x + TILE_SIZE, y + TILE_SIZE))

    # Cerrar imagen original ahora que ya tenemos el crop (evitar resource leak)
    full_image.close()

    # Convertir a RGBA (requerido por Arcade 4.0)
    if sprite_image.mode != "RGBA":
        converted = sprite_image.convert("RGBA")
        sprite_image.close()  # Cerrar la imagen del crop antes de reasignar
        sprite_image = converted

    # Convertir a textura de Arcade 4.0 (no requiere nombre)
    texture = arcade.Texture(image=sprite_image)

    # Guardar en cache
    _texturas_cache[cache_key] = texture

    sprite.texture = texture
    sprite.scale = config.get("scale", 1.0)

    return sprite


def cargar_sprite_jugador() -> arcade.Sprite:
    """Carga el sprite del jugador desde el spritesheet de personajes."""
    return cargar_sprite(JUGADOR, SPRITESHEET_CHARACTERS)


def cargar_sprite_enemigo(tipo: str) -> arcade.Sprite:
    """Carga sprite de enemigo según tipo desde el spritesheet de personajes."""
    if tipo == "jefe":
        return cargar_sprite(JEFE, SPRITESHEET_CHARACTERS)
    elif tipo == "volador":
        return cargar_sprite(ENEMIGO_VOLADOR, SPRITESHEET_CHARACTERS)
    else:
        return cargar_sprite(ENEMIGO_TERRESTRE, SPRITESHEET_CHARACTERS)


def cargar_sprite_item() -> arcade.Sprite:
    """Carga sprite para items/tesoros desde el spritesheet de tiles."""
    return cargar_sprite(TESORO, SPRITESHEET_TILES)


def cargar_sprite_proyectil(es_enemigo: bool = False) -> arcade.Sprite:
    """Carga sprite para proyectiles desde el spritesheet de tiles."""
    if es_enemigo:
        return cargar_sprite(PROYECTIL_ENEMIGO, SPRITESHEET_TILES)
    return cargar_sprite(PROYECTIL_JUGADOR, SPRITESHEET_TILES)
