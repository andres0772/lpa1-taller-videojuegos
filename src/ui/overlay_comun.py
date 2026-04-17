"""Utilidades visuales compartidas por menús superpuestos (pausa, tienda, etc.)."""

from __future__ import annotations

import arcade

# Coherente con el HUD: verdoso oscuro semitransparente
COLOR_RELLENO_PANEL = (26, 34, 28, 200)
COLOR_BORDE_PANEL = (88, 100, 82)
COLOR_TITULO = (236, 210, 132)
COLOR_TEXTO = (228, 232, 224)
COLOR_ATENUADO = (150, 158, 148)
COLOR_ACENTO_OK = (140, 200, 155)
COLOR_ACENTO_PELIGRO = (220, 120, 115)
COLOR_ACENTO_INFO = (160, 200, 215)
_COLOR_BORDE_TEXTO = (14, 16, 12)


def rect_lrbt_centro(cx: float, cy: float, ancho: float, alto: float) -> tuple[float, float, float, float]:
    """left, right, bottom, top (convención lrbt de Arcade)."""
    izq = cx - ancho / 2
    der = cx + ancho / 2
    arriba = cy + alto / 2
    abajo = cy - alto / 2
    return izq, der, abajo, arriba  # CORREGIDO: bottom (abajo) antes que top (arriba)


def dibujar_panel_centrado(cx: float, cy: float, ancho: float, alto: float) -> tuple[float, float, float, float]:
    """Dibuja panel y devuelve (left, right, bottom, top) para colocar texto."""
    izq, der, abajo, arriba = rect_lrbt_centro(cx, cy, ancho, alto)
    arcade.draw_lrbt_rectangle_filled(izq, der, abajo, arriba, COLOR_RELLENO_PANEL)
    arcade.draw_lrbt_rectangle_outline(izq, der, abajo, arriba, COLOR_BORDE_PANEL, border_width=2)
    return izq, der, abajo, arriba


def texto_legible(
    texto: str,
    x: float,
    y: float,
    color,
    tamano: int,
    *,
    anchor_x: str = "left",
    anchor_y: str = "baseline",
    bold: bool = False,
) -> None:
    """Texto claro con contorno oscuro (fondos oscuros semitransparentes)."""
    for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
        arcade.draw_text(
            texto,
            x + ox,
            y + oy,
            _COLOR_BORDE_TEXTO,
            tamano,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            bold=bold,
        )
    arcade.draw_text(
        texto,
        x,
        y,
        color,
        tamano,
        anchor_x=anchor_x,
        anchor_y=anchor_y,
        bold=bold,
    )


def dibujar_separador_horizontal(cx: float, y: float, ancho_util: float, grosor: int = 1) -> None:
    """Línea sutil bajo el título (sin cruzar el texto si y está por debajo del título)."""
    mitad = ancho_util / 2 - 24
    arcade.draw_line(
        cx - mitad,
        y,
        cx + mitad,
        y,
        (64, 72, 60),
        grosor,
    )
