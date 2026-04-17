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


def cargar_sprite(config: dict, sheet_path: str) -> arcade.Sprite:
    """
    Carga un sprite desde el spritesheet.

    Args:
        config: Diccionario con 'row', 'col', 'scale'
        sheet_path: Ruta al spritesheet PNG

    Returns:
        arcade.Sprite configurado
    """
    sprite = arcade.Sprite()

    # Cargar la imagen completa con PIL
    full_image = Image.open(sheet_path)

    # Calcular posición en el spritesheet
    x = config["col"] * TILE_STEP
    y = config["row"] * TILE_STEP

    # Recortar la región del sprite
    sprite_image = full_image.crop((x, y, x + TILE_SIZE, y + TILE_SIZE))
    
    # Convertir a RGBA (requerido por Arcade 4.0)
    if sprite_image.mode != "RGBA":
        sprite_image = sprite_image.convert("RGBA")

    # Convertir a textura de Arcade 4.0 (no requiere nombre)
    texture = arcade.Texture(image=sprite_image)
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
