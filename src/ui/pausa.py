"""UI del menú de pausa."""

import arcade


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
            return True  # Señal para cerrar
        elif key in (arcade.key.NUM_2, arcade.key.KEY_2):
            self._modo_actual = "stats"
            return True
        elif key in (arcade.key.NUM_3, arcade.key.KEY_3):
            # Configuración (simple - por ahora solo vuelve)
            print("Configuración no implementada aún")
            return True
        elif key in (arcade.key.NUM_4, arcade.key.KEY_4):
            # Salir del juego
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
        # Fondo del panel
        ancho = 400
        alto = 350
        x = ANCHO_VENTANA // 2
        y = ALTO_VENTANA // 2

        arcade.draw_lrbt_rectangle_filled(
            left=x - ancho // 2,
            right=x + ancho // 2,
            top=y + alto // 2,
            bottom=y - alto // 2,
            color=(0, 0, 0, 230),
        )

        # Borde
        arcade.draw_lrbt_rectangle_outline(
            left=x - ancho // 2,
            right=x + ancho // 2,
            top=y + alto // 2,
            bottom=y - alto // 2,
            color=arcade.color.CYAN,
            border_width=3,
        )

        # Título
        arcade.draw_text(
            "PAUSA",
            x,
            y + alto // 2 - 30,
            arcade.color.CYAN,
            28,
            anchor_x="center",
            anchor_y="top",
            bold=True,
        )

        # Dividir visual
        arcade.draw_line(
            x - ancho // 2 + 20,
            y + alto // 2 - 50,
            x + ancho // 2 - 20,
            y + alto // 2 - 50,
            arcade.color.GRAY,
            1,
        )

        # Opciones del menú
        y_inicio = y + alto // 2 - 80

        opciones = [
            ("[1] Continuar juego", arcade.color.GREEN),
            ("[2] Stats del personaje", arcade.color.WHITE),
            ("[3] Configuracion", arcade.color.GRAY),
            ("[4] Salir del juego", arcade.color.RED),
        ]

        for i, (texto, color) in enumerate(opciones):
            arcade.draw_text(
                texto,
                x - 120,
                y_inicio - i * 45,
                color,
                16,
                anchor_x="left",
            )

        # Instrucciones
        arcade.draw_text(
            "Presiona el numero de opcion | [ESC] para cancelar",
            x,
            y - alto // 2 + 30,
            arcade.color.GRAY,
            12,
            anchor_x="center",
            anchor_y="bottom",
        )

    def _dibujar_menu_stats(self) -> None:
        """Dibuja el submenú de stats del personaje."""
        # Fondo del panel más grande para stats
        ancho = 450
        alto = 420
        x = ANCHO_VENTANA // 2
        y = ALTO_VENTANA // 2

        arcade.draw_lrbt_rectangle_filled(
            left=x - ancho // 2,
            right=x + ancho // 2,
            top=y + alto // 2,
            bottom=y - alto // 2,
            color=(0, 0, 0, 230),
        )

        arcade.draw_lrbt_rectangle_outline(
            left=x - ancho // 2,
            right=x + ancho // 2,
            top=y + alto // 2,
            bottom=y - alto // 2,
            color=arcade.color.GOLD,
            border_width=3,
        )

        # Título
        arcade.draw_text(
            "STATS DEL PERSONAJE",
            x,
            y + alto // 2 - 30,
            arcade.color.GOLD,
            24,
            anchor_x="center",
            anchor_y="top",
            bold=True,
        )

        # Información del personaje
        y_inicio = y + alto // 2 - 70

        # Stats principales
        stats_info = [
            (f"Nombre: {self._personaje.nombre}", arcade.color.WHITE),
            (f"Nivel: {self._personaje.nivel}", arcade.color.GOLD),
            (
                f"HP: {self._personaje.hp_actual}/{self._personaje.hp_max}",
                arcade.color.GREEN,
            ),
            (
                f"Ataque: {self._personaje.ataque_total} (base: {self._personaje.ataque})",
                arcade.color.RED,
            ),
            (
                f"Defensa: {self._personaje.defensa_total} (base: {self._personaje.defensa})",
                arcade.color.BLUE,
            ),
            (f"Oro: {self._personaje.oro}", arcade.color.YELLOW),
            (
                f"XP: {self._personaje.experiencia}/{self._personaje.experiencia_siguiente_nivel}",
                arcade.color.CYAN,
            ),
        ]

        for i, (texto, color) in enumerate(stats_info):
            arcade.draw_text(
                texto,
                x - 150,
                y_inicio - i * 30,
                color,
                14,
                anchor_x="left",
            )

        # Equipamiento actual
        y_equipo = y_inicio - len(stats_info) * 30 - 20

        arcade.draw_text(
            "EQUIPAMIENTO:",
            x - 150,
            y_equipo,
            arcade.color.PURPLE,
            14,
            anchor_x="left",
            bold=True,
        )

        y_equipo -= 25
        arma = self._personaje.arma_equipada
        armadura = self._personaje.armadura_equipada

        if arma:
            arcade.draw_text(
                f"Espada: {arma.nombre} (+{arma.bonus})",
                x - 150,
                y_equipo,
                arcade.color.WHITE,
                14,
                anchor_x="left",
            )
        else:
            arcade.draw_text(
                "Espada: (ninguna)",
                x - 150,
                y_equipo,
                arcade.color.GRAY,
                14,
                anchor_x="left",
            )

        y_equipo -= 25
        if armadura:
            arcade.draw_text(
                f"Armadura: {armadura.nombre} (+{armadura.bonus})",
                x - 150,
                y_equipo,
                arcade.color.WHITE,
                14,
                anchor_x="left",
            )
        else:
            arcade.draw_text(
                "Armadura: (ninguna)",
                x - 150,
                y_equipo,
                arcade.color.GRAY,
                14,
                anchor_x="left",
            )

        # Inventario
        y_inv = y_equipo - 40

        arcade.draw_text(
            f"INVENTARIO ({len(self._personaje.inventario)} items):",
            x - 150,
            y_inv,
            arcade.color.ORANGE,
            14,
            anchor_x="left",
            bold=True,
        )

        inventario = self._personaje.inventario[:6]  # Mostrar max 6
        y_inv -= 25
        for i, item in enumerate(inventario):
            tipo_icon = "S" if item.tipo == "arma" else "A"
            arcade.draw_text(
                f"  - {tipo_icon} {item.nombre} (+{item.bonus})",
                x - 150,
                y_inv - i * 22,
                arcade.color.WHITE,
                12,
                anchor_x="left",
            )

        if not inventario:
            arcade.draw_text(
                "  (vacio)",
                x - 150,
                y_inv,
                arcade.color.GRAY,
                12,
                anchor_x="left",
            )

        # Instrucciones para volver
        arcade.draw_text(
            "Presiona [ESC] para volver al menu",
            x,
            y - alto // 2 + 30,
            arcade.color.GRAY,
            12,
            anchor_x="center",
            anchor_y="bottom",
        )
