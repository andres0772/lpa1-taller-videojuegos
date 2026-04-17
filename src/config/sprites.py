"""Configuración de sprites del spritesheet de Kenney.

Kenney tiene DOS spritesheets:
1. roguelikeChar_transparent.png - Personajes y enemigos
2. roguelikeSheet_transparent.png - Tiles, items, ambiente

Dimensiones:
- Tiles de 16x16 con 1px de margen (17x17 píxeles por tile).
- Posiciones (fila, columna) son 0-indexed.

NOTA: Estos valores son PLACEHOLDERS. Usar Cursor para identificar
las posiciones reales de cada sprite.
"""

from pathlib import Path

# Ruta base
BASE_PATH = Path(__file__).parent.parent.parent / "assets" / "Spritesheet"

# Spritesheet de PERSONAJES (héroes, enemigos)
SPRITESHEET_CHARACTERS = str(BASE_PATH / "roguelikeChar_transparent.png")

# Spritesheet de TILES (items, ambiente, proyectiles)
SPRITESHEET_TILES = str(BASE_PATH / "roguelikeSheet_transparent.png")

# Dimensiones del spritesheet
TILE_SIZE = 16
MARGIN = 1
TILE_STEP = TILE_SIZE + MARGIN  # 17 píxeles entre cada sprite

# ============================================
# PERSONAJES (de roguelikeChar_transparent.png)
# Identificados con Cursor - 2026-04-17
# ============================================

JUGADOR = {"row": 2, "col": 1, "scale": 2.0}  # Aventurero/caballero
ENEMIGO_TERRESTRE = {"row": 5, "col": 1, "scale": 2.0}  # Demonio/esqueleto
ENEMIGO_VOLADOR = {"row": 6, "col": 1, "scale": 2.0}  # Murciélago
JEFE = {"row": 5, "col": 0, "scale": 2.5}  # Jefe demonio

# ============================================
# TILES E ITEMS (de roguelikeSheet_transparent.png)
# Identificados con Cursor - 2026-04-17
# ============================================

TESORO = {"row": 8, "col": 35, "scale": 1.5}  # Cofre/tesoro
PROYECTIL_JUGADOR = {"row": 28, "col": 52, "scale": 1.0}  # Flecha
PROYECTIL_ENEMIGO = {"row": 27, "col": 52, "scale": 1.0}  # Orbe enemigo

# Tiles de ambiente (opcional, para futuras mejoras)
SUELO = {"row": 0, "col": 0, "scale": 1.0}
PARED = {"row": 0, "col": 1, "scale": 1.0}
ANTORCHA = {"row": 0, "col": 2, "scale": 1.0}
