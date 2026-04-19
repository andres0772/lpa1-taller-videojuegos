"""UI del menú de pausa."""

import arcade

from src.sistemas.audio import GestorAudio
from .overlay_comun import (
    COLOR_ACENTO_INFO,
    COLOR_ACENTO_OK,
    COLOR_ACENTO_PELIGRO,
    COLOR_ATENUADO,
    COLOR_TITULO,
    COLOR_TEXTO,
    dibujar_panel_centrado,
    dibujar_separador_horizontal,
    texto_legible,
)

# Variables globales para dimensiones (para evitar imports circulares)
ANCHO_VENTANA = 1080
ALTO_VENTANA = 720


class MenuPausa:
    """Menú de pausa del juego."""

    def __init__(self, personaje):
        self._personaje = personaje
        self._modo_actual = "menu"  # menu | stats

    @property
    def abierto(self) -> bool:
        return True  # Siempre está disponible cuando se abre desde el juego

    def abrir(self) -> None:
        """Abre el menú de pausa."""
        self._modo_actual = "menu"
        GestorAudio.reproducir_ui()

    def cerrar(self) -> None:
        """Cierra el menú de pausa."""
        self._modo_actual = "menu"

    def manejar_input(self, key) -> bool:
        """Maneja input del teclado. Retorna True si se procesó input."""
        if self._modo_actual == "menu":
            return self._manejar_menu(key)
        elif self._modo_actual == "stats":
            return self._manejar_stats(key)
        return False

    def _manejar_menu(self, key) -> bool:
        """Maneja el menú principal."""
        if key in (arcade.key.NUM_1, arcade.key.KEY_1):
            # Continuar juego - cerrar menú
            GestorAudio.reproducir_ui()
            return True  # Señal para cerrar
        elif key in (arcade.key.NUM_2, arcade.key.KEY_2):
            GestorAudio.reproducir_ui()
            self._modo_actual = "stats"
            return True
        elif key in (arcade.key.NUM_3, arcade.key.KEY_3):
            # Configuración (simple - por ahora solo vuelve)
            GestorAudio.reproducir_ui()
            print("Configuración no implementada aún")
            return True
        elif key in (arcade.key.NUM_4, arcade.key.KEY_4):
            # Salir del juego
            GestorAudio.reproducir_ui()
            print("Saliendo del juego...")
            arcade.close_window()
            return True
        return False

    def _manejar_stats(self, key) -> bool:
        """Maneja el submenú de stats."""
        if key == arcade.key.ESCAPE:
            self._modo_actual = "menu"
            return True
        return False

    def dibujar(self) -> None:
        """Dibuja el menú de pausa."""
        if self._modo_actual == "menu":
            self._dibujar_menu_principal()
        elif self._modo_actual == "stats":
            self._dibujar_menu_stats()

    def _dibujar_menu_principal(self) -> None:
        """Dibuja el menú principal de pausa."""
        ancho = 420
        alto = 360
        x = ANCHO_VENTANA // 2
        y = ALTO_VENTANA // 2
        _, _, _, arriba = dibujar_panel_centrado(x, y, ancho, alto)

        texto_legible(
            "PAUSA",
            x,
            arriba - 20,
            COLOR_TITULO,
            26,
            anchor_x="center",
            anchor_y="top",
            bold=True,
        )
        # Debajo del título (evita la línea cortando las letras)
        dibujar_separador_horizontal(x, arriba - 52, ancho)

        y_opc = arriba - 78
        espacio = 42
        opciones: list[tuple[str, tuple[int, int, int]]] = [
            ("1  ·  Continuar juego", COLOR_ACENTO_OK),
            ("2  ·  Stats del personaje", COLOR_TEXTO),
            ("3  ·  Configuración", COLOR_ATENUADO),
            ("4  ·  Salir del juego", COLOR_ACENTO_PELIGRO),
        ]
        for i, (texto, color) in enumerate(opciones):
            texto_legible(
                texto,
                x,
                y_opc - i * espacio,
                color,
                16,
                anchor_x="center",
                anchor_y="top",
            )

        texto_legible(
            "Número de opción  ·  [ESC] volver al juego",
            x,
            y - alto // 2 + 28,
            COLOR_ATENUADO,
            12,
            anchor_x="center",
            anchor_y="bottom",
        )

    def _dibujar_menu_stats(self) -> None:
        """Dibuja el submenú de stats del personaje."""
        ancho = 460
        alto = 440
        x = ANCHO_VENTANA // 2
        y = ALTO_VENTANA // 2
        _, _, _, arriba = dibujar_panel_centrado(x, y, ancho, alto)

        texto_legible(
            "Personaje",
            x,
            arriba - 20,
            COLOR_TITULO,
            22,
            anchor_x="center",
            anchor_y="top",
            bold=True,
        )
        dibujar_separador_horizontal(x, arriba - 48, ancho)

        y_inicio = arriba - 72
        interlineado = 26

        stats_info: list[tuple[str, tuple[int, int, int]]] = [
            (f"Nombre: {self._personaje.nombre}", COLOR_TEXTO),
            (f"Nivel: {self._personaje.nivel}", COLOR_TITULO),
            (
                f"HP: {self._personaje.hp_actual} / {self._personaje.hp_max}",
                COLOR_ACENTO_OK,
            ),
            (
                f"Ataque: {self._personaje.ataque_total}  (base {self._personaje.ataque})",
                COLOR_ACENTO_PELIGRO,
            ),
            (
                f"Defensa: {self._personaje.defensa_total}  (base {self._personaje.defensa})",
                COLOR_ACENTO_INFO,
            ),
            (f"Oro: {self._personaje.oro}", COLOR_TITULO),
            (
                f"XP: {self._personaje.experiencia} / {self._personaje.experiencia_siguiente_nivel}",
                COLOR_ATENUADO,
            ),
        ]

        for i, (texto, color) in enumerate(stats_info):
            texto_legible(
                texto,
                x - 170,
                y_inicio - i * interlineado,
                color,
                14,
                anchor_x="left",
                anchor_y="top",
            )

        y_equipo = y_inicio - len(stats_info) * interlineado - 16
        texto_legible(
            "Equipamiento",
            x - 170,
            y_equipo,
            COLOR_TITULO,
            14,
            anchor_x="left",
            anchor_y="top",
            bold=True,
        )

        y_equipo -= interlineado
        arma = self._personaje.arma_equipada
        armadura = self._personaje.armadura_equipada

        if arma:
            texto_legible(
                f"Arma: {arma.nombre}  (+{arma.bonus})",
                x - 170,
                y_equipo,
                COLOR_TEXTO,
                13,
                anchor_x="left",
                anchor_y="top",
            )
        else:
            texto_legible(
                "Arma: (ninguna)",
                x - 170,
                y_equipo,
                COLOR_ATENUADO,
                13,
                anchor_x="left",
                anchor_y="top",
            )

        y_equipo -= interlineado - 2
        if armadura:
            texto_legible(
                f"Armadura: {armadura.nombre}  (+{armadura.bonus})",
                x - 170,
                y_equipo,
                COLOR_TEXTO,
                13,
                anchor_x="left",
                anchor_y="top",
            )
        else:
            texto_legible(
                "Armadura: (ninguna)",
                x - 170,
                y_equipo,
                COLOR_ATENUADO,
                13,
                anchor_x="left",
                anchor_y="top",
            )

        y_inv = y_equipo - interlineado - 10
        texto_legible(
            f"Inventario  ({len(self._personaje.inventario)} ítems)",
            x - 170,
            y_inv,
            COLOR_TITULO,
            14,
            anchor_x="left",
            anchor_y="top",
            bold=True,
        )

        inventario = self._personaje.inventario[:6]
        y_inv -= interlineado
        for i, item in enumerate(inventario):
            tipo_icon = "S" if item.tipo == "arma" else "A"
            texto_legible(
                f"  ·  [{tipo_icon}] {item.nombre}  (+{item.bonus})",
                x - 170,
                y_inv - i * 22,
                COLOR_TEXTO,
                12,
                anchor_x="left",
                anchor_y="top",
            )

        if not inventario:
            texto_legible(
                "  (vacío)",
                x - 170,
                y_inv,
                COLOR_ATENUADO,
                12,
                anchor_x="left",
                anchor_y="top",
            )

        texto_legible(
            "[ESC] Volver al menú de pausa",
            x,
            y - alto // 2 + 28,
            COLOR_ATENUADO,
            12,
            anchor_x="center",
            anchor_y="bottom",
        )
