"""UI de la tienda."""

import arcade
from ..sistemas.tienda import SistemaTienda


class MenuTienda:
    """Menú de la tienda可视化."""

    def __init__(self, personaje, escenario):
        self._personaje = personaje
        self._escenario = escenario
        self._modo_actual = "menu"  # menu | comprar | vender
        self._mensaje = ""
        self._mostrar_mensaje_timer = 0.0

    @property
    def abierto(self) -> bool:
        return self._modo_actual != "menu"

    def abrir(self) -> None:
        """Abre el menú de la tienda."""
        self._modo_actual = "menu"
        self._mensaje = ""

    def cerrar(self) -> None:
        """Cierra el menú de la tienda."""
        self._modo_actual = "menu"
        self._mensaje = ""

    def manejar_input(self, key) -> bool:
        """Maneja input del teclado. Retorna True si se dibujó algo."""
        if self._modo_actual == "menu":
            return self._manejar_menu(key)
        elif self._modo_actual == "comprar":
            return self._manejar_comprar(key)
        elif self._modo_actual == "vender":
            return self._manejar_vender(key)
        return False

    def _manejar_menu(self, key) -> bool:
        """Maneja el menú principal."""
        if key in (arcade.key.NUM_1, arcade.key.KEY_1):
            self._modo_actual = "comprar"
            self._mensaje = ""
            return True
        elif key in (arcade.key.NUM_2, arcade.key.KEY_2):
            self._modo_actual = "vender"
            self._mensaje = ""
            if not self._personaje.inventario:
                self._mensaje = "Inventario vacío"
            return True
        elif key in (arcade.key.NUM_3, arcade.key.KEY_3):
            # Equipar items del inventario
            self._mensaje = self._equipar_items()
            self._mostrar_mensaje_timer = 2.0
            return True
        elif key in (arcade.key.ESCAPE, arcade.key.NUM_4, arcade.key.KEY_4):
            self.cerrar()
            return True
        return False

    def _manejar_comprar(self, key) -> bool:
        """Maneja el menú de compra."""
        # Mapeo de teclas a índice (1-9)
        mapeo = {
            arcade.key.NUM_1: 0,
            arcade.key.KEY_1: 0,
            arcade.key.NUM_2: 1,
            arcade.key.KEY_2: 1,
            arcade.key.NUM_3: 2,
            arcade.key.KEY_3: 2,
            arcade.key.NUM_4: 3,
            arcade.key.KEY_4: 3,
            arcade.key.NUM_5: 4,
            arcade.key.KEY_5: 4,
        }

        if key in mapeo:
            indice = mapeo[key]
            exito, mensaje = SistemaTienda.comprar_item(indice, self._personaje)
            self._mensaje = mensaje
            self._mostrar_mensaje_timer = 2.0
            return True
        elif key == arcade.key.ESCAPE:
            self._modo_actual = "menu"
            self._mensaje = ""
            return True
        return False

    def _manejar_vender(self, key) -> bool:
        """Maneja el menú de venta."""
        # El jugador presiona 1-9 para vender el item en ese índice
        if self._personaje.inventario:
            # Calcular índice basado en tecla
            mapeo = {
                arcade.key.NUM_1: 0,
                arcade.key.KEY_1: 0,
                arcade.key.NUM_2: 1,
                arcade.key.KEY_2: 1,
                arcade.key.NUM_3: 2,
                arcade.key.KEY_3: 2,
                arcade.key.NUM_4: 3,
                arcade.key.KEY_4: 3,
                arcade.key.NUM_5: 4,
                arcade.key.KEY_5: 4,
                arcade.key.NUM_6: 5,
                arcade.key.KEY_6: 5,
                arcade.key.NUM_7: 6,
                arcade.key.KEY_7: 6,
                arcade.key.NUM_8: 7,
                arcade.key.KEY_8: 7,
                arcade.key.NUM_9: 8,
                arcade.key.KEY_9: 8,
            }

            if key in mapeo:
                indice = mapeo[key]
                if indice < len(self._personaje.inventario):
                    exito, mensaje = SistemaTienda.vender_item(indice, self._personaje)
                    self._mensaje = mensaje
                    self._mostrar_mensaje_timer = 2.0

                    # Si quedó vacío, volver al menú
                    if not self._personaje.inventario:
                        self._mensaje = "Inventario vacío"
                    return True

        if key == arcade.key.ESCAPE:
            self._modo_actual = "menu"
            self._mensaje = ""
            return True
        return False

    def _equipar_items(self) -> str:
        """Equipa items automáticamente."""
        equips_arma = []
        equips_armadura = []

        # Separar por tipo
        for item in self._personaje.inventario:
            if hasattr(item, "tipo"):
                if item.tipo == "arma":
                    equips_arma.append(item)
                elif item.tipo == "armadura":
                    equips_armadura.append(item)

        # Equipar el mejor de cada tipo
        mejor_arma = None
        mejor_bonus_arma = -1
        for equip in equips_arma:
            if equip.bonus > mejor_bonus_arma:
                mejor_bonus_arma = equip.bonus
                mejor_arma = equip

        mejor_armadura = None
        mejor_bonus_armadura = -1
        for equip in equips_armadura:
            if equip.bonus > mejor_bonus_armadura:
                mejor_bonus_armadura = equip.bonus
                mejor_armadura = equip

        # Equipar
        if mejor_arma:
            self._personaje.equipar(mejor_arma)
        if mejor_armadura:
            self._personaje.equipar(mejor_armadura)

        # Resumen
        resumen = []
        if mejor_arma:
            resumen.append(f"Espada: {mejor_arma.nombre} (+{mejor_arma.bonus})")
        if mejor_armadura:
            resumen.append(
                f"Armadura: {mejor_armadura.nombre} (+{mejor_armadura.bonus})"
            )

        if not resumen:
            return "No hay equipamiento en inventario"
        return "Equipado: " + ", ".join(resumen)

    def dibujar(self) -> None:
        """Dibuja el menú de la tienda si está abierto."""
        if self._modo_actual == "menu":
            self._dibujar_menu_principal()
        elif self._modo_actual == "comprar":
            self._dibujar_menu_comprar()
        elif self._modo_actual == "vender":
            self._dibujar_menu_vender()

    def _dibujar_menu_principal(self) -> None:
        """Dibuja el menú principal de la tienda."""
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
            color=(0, 0, 0, 220),
        )

        # Borde
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
            "🛒 TIENDA",
            x,
            y + alto // 2 - 20,
            arcade.color.GOLD,
            24,
            anchor_x="center",
            anchor_y="top",
            bold=True,
        )

        # Oro del jugador
        arcade.draw_text(
            f"Tu oro: {self._personaje.oro} 💰",
            x,
            y + alto // 2 - 50,
            arcade.color.YELLOW,
            16,
            anchor_x="center",
            anchor_y="top",
        )

        # Opciones (con mayor espaciado entre líneas)
        opciones = [
            ("[1] Comprar equipamiento", 0, arcade.color.WHITE),
            ("", -25, arcade.color.BLACK),  # Línea en blanco
            ("[2] Vender items del inventario", -45, arcade.color.WHITE),
            ("", -65, arcade.color.BLACK),  # Línea en blanco
            ("[3] Equipar mejores items", -85, arcade.color.CYAN),
            ("", -105, arcade.color.BLACK),  # Línea en blanco
            ("[4] Salir / ESC", -125, arcade.color.GRAY),
        ]

        for texto, desfase, color in opciones:
            arcade.draw_text(
                texto,
                x - 120,
                y + alto // 2 - 75 + desfase,
                color,
                16,
                anchor_x="left",
            )

        # Stats actuales
        arcade.draw_text(
            f"ATAQUE: {self._personaje.ataque_total} | DEFENSA: {self._personaje.defensa_total}",
            x,
            y - alto // 2 + 30,
            arcade.color.GREEN,
            14,
            anchor_x="center",
            anchor_y="bottom",
        )

        # Mensaje de feedback
        if self._mensaje:
            arcade.draw_text(
                self._mensaje,
                x,
                y - alto // 2 + 60,
                arcade.color.LIGHT_GREEN if "¡" in self._mensaje else arcade.color.RED,
                14,
                anchor_x="center",
                anchor_y="bottom",
            )

    def _dibujar_menu_comprar(self) -> None:
        """Dibuja el menú de compra."""
        # Fondo del panel
        ancho = 450
        alto = 400
        x = ANCHO_VENTANA // 2
        y = ALTO_VENTANA // 2

        arcade.draw_lrbt_rectangle_filled(
            left=x - ancho // 2,
            right=x + ancho // 2,
            top=y + alto // 2,
            bottom=y - alto // 2,
            color=(0, 0, 0, 220),
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
            "💰 COMPRAR EQUIPAMIENTO",
            x,
            y + alto // 2 - 30,
            arcade.color.GOLD,
            22,
            anchor_x="center",
            anchor_y="top",
            bold=True,
        )

        # Oro
        arcade.draw_text(
            f"Oro disponible: {self._personaje.oro} 💰",
            x,
            y + alto // 2 - 60,
            arcade.color.YELLOW,
            14,
            anchor_x="center",
            anchor_y="top",
        )

        # Items en venta
        items = SistemaTienda.getter_items_tienda()
        for i, item in enumerate(items):
            # Color según stock y precio
            color = arcade.color.WHITE
            if item.stock <= 0:
                color = arcade.color.GRAY
            elif self._personaje.oro < item.precio:
                color = arcade.color.RED

            tipo_icon = "⚔️" if item.tipo == "arma" else "🛡️"
            nombre = f"[{i + 1}] {tipo_icon} {item.nombre}"
            detalle = f"+{item.bonus} {item.tipo} - {item.precio}g"

            arcade.draw_text(
                nombre, x - 150, y + alto // 2 - 95 - i * 30, color, 14, anchor_x="left"
            )
            arcade.draw_text(
                detalle, x + 50, y + alto // 2 - 95 - i * 30, color, 14, anchor_x="left"
            )

        # Instrucciones
        arcade.draw_text(
            "Presiona [1-4] para comprar, [ESC] para volver",
            x,
            y - alto // 2 + 30,
            arcade.color.GRAY,
            12,
            anchor_x="center",
            anchor_y="bottom",
        )

        # Mensaje
        if self._mensaje:
            color = (
                arcade.color.LIGHT_GREEN if "¡" in self._mensaje else arcade.color.RED
            )
            arcade.draw_text(
                self._mensaje,
                x,
                y - alto // 2 + 60,
                color,
                14,
                anchor_x="center",
                anchor_y="bottom",
            )

    def _dibujar_menu_vender(self) -> None:
        """Dibuja el menú de venta."""
        # Fondo del panel
        ancho = 450
        alto = 400
        x = ANCHO_VENTANA // 2
        y = ALTO_VENTANA // 2

        arcade.draw_lrbt_rectangle_filled(
            left=x - ancho // 2,
            right=x + ancho // 2,
            top=y + alto // 2,
            bottom=y - alto // 2,
            color=(0, 0, 0, 220),
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
            "💵 VENDER ITEMS",
            x,
            y + alto // 2 - 30,
            arcade.color.GOLD,
            22,
            anchor_x="center",
            anchor_y="top",
            bold=True,
        )

        # Oro actual
        arcade.draw_text(
            f"Oro actual: {self._personaje.oro} 💰",
            x,
            y + alto // 2 - 60,
            arcade.color.YELLOW,
            14,
            anchor_x="center",
            anchor_y="top",
        )

        # Inventario
        inventario = self._personaje.inventario
        if inventario:
            for i, item in enumerate(inventario[:8]):  # Máximo 8 items visbles
                tipo_icon = "⚔️" if item.tipo == "arma" else "🛡️"
                valor_venta = item.vender()
                nombre = f"[{i + 1}] {tipo_icon} {item.nombre}"
                detalle = f"+{item.bonus} {item.tipo} = {valor_venta}g"

                arcade.draw_text(
                    nombre,
                    x - 150,
                    y + alto // 2 - 95 - i * 30,
                    arcade.color.WHITE,
                    14,
                    anchor_x="left",
                )
                arcade.draw_text(
                    detalle,
                    x + 50,
                    y + alto // 2 - 95 - i * 30,
                    arcade.color.YELLOW,
                    14,
                    anchor_x="left",
                )
        else:
            arcade.draw_text(
                "Inventario vacío",
                x,
                y,
                arcade.color.RED,
                16,
                anchor_x="center",
                anchor_y="center",
            )

        # Instrucciones
        arcade.draw_text(
            "Presiona [1-8] para vender item, [ESC] para volver",
            x,
            y - alto // 2 + 30,
            arcade.color.GRAY,
            12,
            anchor_x="center",
            anchor_y="bottom",
        )

        # Mensaje
        if self._mensaje:
            color = (
                arcade.color.LIGHT_GREEN if "¡" in self._mensaje else arcade.color.RED
            )
            arcade.draw_text(
                self._mensaje,
                x,
                y - alto // 2 + 60,
                color,
                14,
                anchor_x="center",
                anchor_y="bottom",
            )


# Variables globales para dimensiones (para evitar imports circulares)
ANCHO_VENTANA = 1080
ALTO_VENTANA = 720
