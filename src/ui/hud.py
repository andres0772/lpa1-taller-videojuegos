"""HUD de estadísticas del personaje (panel semitransparente, sin tiles decorativos)."""

import arcade

# Tamaño y posición del bloque de stats (misma área útil que antes, en píxeles)
TILE_UNIT = 32
PANEL_ANCHO_TILES = 10
PANEL_ALTO_TILES = 5
PANEL_POS_X = 12
PANEL_POS_Y = 12

# Panel semitransparente: el mapa se ve un poco detrás y no tapa tanto como el crema opaco
_ALPHA_FONDO = 175
_COLOR_FONDO_PANEL = (26, 34, 28, _ALPHA_FONDO)
_COLOR_BORDE_PANEL = (72, 84, 70, 220)

_COLOR_TEXTO_TITULO = (246, 244, 238)
_COLOR_TEXTO_SEC = (198, 204, 194)
_COLOR_ORO = (238, 206, 120)
_COLOR_XP_ETIQUETA = (214, 190, 242)
_COLOR_XP_RELLENO = (120, 82, 168)
_COLOR_BARRA_FONDO = (52, 48, 58)
_COLOR_BARRA_BORDE = (32, 28, 36)


class HUD:
    """Muestra nombre, nivel, oro, vida y experiencia sobre un panel simple."""

    def __init__(self, personaje):
        self._personaje = personaje

    @staticmethod
    def _dibujar_texto_legible(
        texto: str,
        x: float,
        y: float,
        color,
        font_size: int,
        *,
        anchor_x: str = "left",
        anchor_y: str = "baseline",
        bold: bool = False,
    ) -> None:
        """Texto con contorno oscuro fino para leerse sobre el panel semitransparente."""
        outline = (12, 14, 12)
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
            arcade.draw_text(
                texto,
                x + ox,
                y + oy,
                outline,
                font_size,
                anchor_x=anchor_x,
                anchor_y=anchor_y,
                bold=bold,
            )
        arcade.draw_text(
            texto,
            x,
            y,
            color,
            font_size,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            bold=bold,
        )

    @staticmethod
    def _dibujar_barra(x: float, y: float, ancho: float, alto: float, ratio: float, color_relleno) -> None:
        """Barra de progreso con fondo oscuro y relleno proporcional al ratio [0, 1]."""
        ratio = max(0.0, min(1.0, ratio))
        arcade.draw_lbwh_rectangle_filled(x, y, ancho, alto, _COLOR_BARRA_FONDO)
        if ratio > 0:
            arcade.draw_lbwh_rectangle_filled(x, y, ancho * ratio, alto, color_relleno)
        arcade.draw_lbwh_rectangle_outline(
            x, y, ancho, alto, _COLOR_BARRA_BORDE, border_width=1
        )

    def dibujar(self) -> None:
        """Dibuja el HUD en pantalla."""
        panel_x = PANEL_POS_X
        panel_y = PANEL_POS_Y
        panel_w = PANEL_ANCHO_TILES * TILE_UNIT
        panel_h = PANEL_ALTO_TILES * TILE_UNIT
        panel_top = panel_y + panel_h
        pad_x = 14
        pad_top = 10

        arcade.draw_lbwh_rectangle_filled(
            panel_x, panel_y, panel_w, panel_h, _COLOR_FONDO_PANEL
        )
        arcade.draw_lbwh_rectangle_outline(
            panel_x, panel_y, panel_w, panel_h, _COLOR_BORDE_PANEL, border_width=2
        )

        self._dibujar_texto_legible(
            f"Héroe  {self._personaje.nombre}",
            panel_x + pad_x,
            panel_top - pad_top,
            _COLOR_TEXTO_TITULO,
            13,
            anchor_x="left",
            anchor_y="top",
            bold=True,
        )

        fila_stats_y = panel_top - pad_top - 24
        self._dibujar_texto_legible(
            f"Nivel {self._personaje.nivel}",
            panel_x + pad_x,
            fila_stats_y,
            _COLOR_TEXTO_SEC,
            12,
            anchor_x="left",
            anchor_y="top",
            bold=True,
        )
        self._dibujar_texto_legible(
            f"Oro  {self._personaje.oro}",
            panel_x + panel_w - pad_x,
            fila_stats_y,
            _COLOR_ORO,
            12,
            anchor_x="right",
            anchor_y="top",
            bold=True,
        )

        bar_h = 11
        bar_left = panel_x + pad_x
        bar_w = panel_w - 2 * pad_x
        inner_right = panel_x + panel_w - pad_x

        hp_max = max(1, self._personaje.hp_max)
        hp_ratio = self._personaje.hp_actual / hp_max
        if self._personaje.hp_actual < hp_max * 0.3:
            hp_fill = (178, 48, 42)
        elif self._personaje.hp_actual < hp_max * 0.55:
            hp_fill = (196, 118, 42)
        else:
            hp_fill = (52, 132, 62)

        xp_need = max(1, self._personaje.experiencia_siguiente_nivel)
        xp_ratio = self._personaje.experiencia / xp_need

        y_hp_etiqueta = panel_top - pad_top - 48
        self._dibujar_texto_legible(
            "Vida",
            bar_left,
            y_hp_etiqueta,
            _COLOR_TEXTO_SEC,
            11,
            anchor_x="left",
            anchor_y="top",
        )
        self._dibujar_texto_legible(
            f"{self._personaje.hp_actual} / {self._personaje.hp_max}",
            inner_right,
            y_hp_etiqueta,
            hp_fill,
            11,
            anchor_x="right",
            anchor_y="top",
            bold=True,
        )
        # Separación clara entre etiqueta (anchor top) y la barra
        y_hp_bar = y_hp_etiqueta - 18 - bar_h
        self._dibujar_barra(bar_left, y_hp_bar, bar_w, bar_h, hp_ratio, hp_fill)

        y_xp_etiqueta = y_hp_bar - 20
        self._dibujar_texto_legible(
            "Experiencia",
            bar_left,
            y_xp_etiqueta,
            _COLOR_XP_ETIQUETA,
            11,
            anchor_x="left",
            anchor_y="top",
        )
        self._dibujar_texto_legible(
            f"{self._personaje.experiencia} / {self._personaje.experiencia_siguiente_nivel}",
            inner_right,
            y_xp_etiqueta,
            _COLOR_XP_ETIQUETA,
            11,
            anchor_x="right",
            anchor_y="top",
            bold=True,
        )
        y_xp_bar = y_xp_etiqueta - 18 - bar_h
        self._dibujar_barra(bar_left, y_xp_bar, bar_w, bar_h, xp_ratio, _COLOR_XP_RELLENO)
