"""UI de la tienda."""

import arcade

from ..sistemas.tienda import SistemaTienda
from .overlay_comun import (
    COLOR_ACENTO_INFO,
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


class MenuTienda:
    """Menú de la tienda."""

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
        elif key in (arcade.key.ESCAPE, arcade.key.NUM_3, arcade.key.KEY_3):
            self.cerrar()
            return True
        return False

    def _manejar_comprar(self, key) -> bool:
        """Maneja el menú de compra."""
        mapeo = {
            arcade.key.NUM_1: 0,
            arcade.key.KEY_1: 0,
            arcade.key.NUM_2: 1,
            arcade.key.KEY_2: 1,
            arcade.key.NUM_3: 2,
            arcade.key.KEY_3: 2,
            arcade.key.NUM_4: 3,
            arcade.key.KEY_4: 3,
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
        if self._personaje.inventario:
            # IMPORTANTE: limitar a 1-8 para coincidir con display (línea 361 muestra hasta 8 items)
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
            }

            if key in mapeo:
                indice = mapeo[key]
                if indice < len(self._personaje.inventario):
                    exito, mensaje = SistemaTienda.vender_item(indice, self._personaje)
                    self._mensaje = mensaje
                    self._mostrar_mensaje_timer = 2.0

                    if not self._personaje.inventario:
                        self._mensaje = "Inventario vacío"
                    return True

        if key == arcade.key.ESCAPE:
            self._modo_actual = "menu"
            self._mensaje = ""
            return True
        return False

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
        ancho = 440
        alto = 400
        x = ANCHO_VENTANA // 2
        y = ALTO_VENTANA // 2
        _, _, abajo, arriba = dibujar_panel_centrado(x, y, ancho, alto)

        texto_legible(
            "TIENDA",
            x,
            arriba - 18,
            COLOR_TITULO,
            24,
            anchor_x="center",
            anchor_y="top",
            bold=True,
        )
        texto_legible(
            f"Tu oro: {self._personaje.oro}",
            x,
            arriba - 50,
            COLOR_TITULO,
            15,
            anchor_x="center",
            anchor_y="top",
        )
        dibujar_separador_horizontal(x, arriba - 62, ancho)

        y_opc = arriba - 88
        espacio = 40
        texto_legible(
            "1  ·  Comprar mejoras",
            x,
            y_opc,
            COLOR_TEXTO,
            16,
            anchor_x="center",
            anchor_y="top",
        )
        texto_legible(
            "2  ·  Vender ítems del inventario",
            x,
            y_opc - espacio,
            COLOR_TEXTO,
            16,
            anchor_x="center",
            anchor_y="top",
        )
        texto_legible(
            "3  ·  Salir   (ESC)",
            x,
            y_opc - 2 * espacio,
            COLOR_ATENUADO,
            16,
            anchor_x="center",
            anchor_y="top",
        )

        texto_legible(
            f"Cooldown {self._personaje.cooldown_disparo:.2f}s  ·  Daño ×{self._personaje.dano_proyectil:.2f}",
            x,
            abajo + 38,
            COLOR_ACENTO_INFO,
            12,
            anchor_x="center",
            anchor_y="bottom",
        )
        texto_legible(
            f"Velocidad proyectil ×{self._personaje.velocidad_proyectil:.2f}  ·  Rebotes {self._personaje.rebotes}",
            x,
            abajo + 20,
            COLOR_ACENTO_INFO,
            12,
            anchor_x="center",
            anchor_y="bottom",
        )

        if self._mensaje:
            color = (
                (150, 210, 160) if "¡" in self._mensaje else COLOR_ACENTO_PELIGRO
            )
            texto_legible(
                self._mensaje,
                x,
                abajo + 58,
                color,
                14,
                anchor_x="center",
                anchor_y="bottom",
            )

    def _dibujar_menu_comprar(self) -> None:
        """Dibuja el menú de compra."""
        ancho = 470
        alto = 420
        x = ANCHO_VENTANA // 2
        y = ALTO_VENTANA // 2
        _, _, abajo, arriba = dibujar_panel_centrado(x, y, ancho, alto)

        texto_legible(
            "Mejoras de proyectiles",
            x,
            arriba - 18,
            COLOR_TITULO,
            20,
            anchor_x="center",
            anchor_y="top",
            bold=True,
        )
        texto_legible(
            f"Oro disponible: {self._personaje.oro}",
            x,
            arriba - 48,
            COLOR_TITULO,
            14,
            anchor_x="center",
            anchor_y="top",
        )
        dibujar_separador_horizontal(x, arriba - 58, ancho)

        items = SistemaTienda.getter_items_tienda()
        iconos = {
            "velocidad_disparo": "[+]",
            "dano_proyectil": "[*]",
            "velocidad_proyectil": "[>]",
            "rebote": "[~]",
        }
        y0 = arriba - 84
        for i, item in enumerate(items):
            color = COLOR_TEXTO
            if item.stock == 0:
                color = COLOR_ATENUADO
            elif self._personaje.oro < item.precio:
                color = COLOR_ACENTO_PELIGRO

            icono = iconos.get(item.tipo, "[·]")
            nombre = f"{i + 1}  ·  {icono}  {item.nombre}"
            detalle = f"{item.precio} g"

            texto_legible(
                nombre,
                x - 175,
                y0 - i * 30,
                color,
                14,
                anchor_x="left",
                anchor_y="top",
            )
            texto_legible(
                detalle,
                x + 120,
                y0 - i * 30,
                color,
                14,
                anchor_x="left",
                anchor_y="top",
            )

        texto_legible(
            "[1-4] Comprar   ·   [ESC] Volver",
            x,
            abajo + 28,
            COLOR_ATENUADO,
            12,
            anchor_x="center",
            anchor_y="bottom",
        )

        if self._mensaje:
            color = (150, 210, 160) if "¡" in self._mensaje else COLOR_ACENTO_PELIGRO
            texto_legible(
                self._mensaje,
                x,
                abajo + 52,
                color,
                14,
                anchor_x="center",
                anchor_y="bottom",
            )

    def _dibujar_menu_vender(self) -> None:
        """Dibuja el menú de venta."""
        ancho = 470
        alto = 420
        x = ANCHO_VENTANA // 2
        y = ALTO_VENTANA // 2
        _, _, abajo, arriba = dibujar_panel_centrado(x, y, ancho, alto)

        texto_legible(
            "Vender ítems",
            x,
            arriba - 18,
            COLOR_TITULO,
            20,
            anchor_x="center",
            anchor_y="top",
            bold=True,
        )
        texto_legible(
            f"Oro actual: {self._personaje.oro}",
            x,
            arriba - 48,
            COLOR_TITULO,
            14,
            anchor_x="center",
            anchor_y="top",
        )
        dibujar_separador_horizontal(x, arriba - 58, ancho)

        inventario = self._personaje.inventario
        y0 = arriba - 84
        if inventario:
            for i, item in enumerate(inventario[:8]):
                tipo_icon = "[A]" if item.tipo == "arma" else "[D]"
                valor_venta = item.vender()
                nombre = f"{i + 1}  ·  {tipo_icon}  {item.nombre}"
                detalle = f"+{item.bonus}  ·  {valor_venta} g"

                texto_legible(
                    nombre,
                    x - 175,
                    y0 - i * 30,
                    COLOR_TEXTO,
                    14,
                    anchor_x="left",
                    anchor_y="top",
                )
                texto_legible(
                    detalle,
                    x + 100,
                    y0 - i * 30,
                    COLOR_TITULO,
                    14,
                    anchor_x="left",
                    anchor_y="top",
                )
        else:
            texto_legible(
                "Inventario vacío",
                x,
                y,
                COLOR_ACENTO_PELIGRO,
                16,
                anchor_x="center",
                anchor_y="center",
            )

        texto_legible(
            "[1-8] Vender   ·   [ESC] Volver",
            x,
            abajo + 28,
            COLOR_ATENUADO,
            12,
            anchor_x="center",
            anchor_y="bottom",
        )

        if self._mensaje:
            color = (150, 210, 160) if "¡" in self._mensaje else COLOR_ACENTO_PELIGRO
            texto_legible(
                self._mensaje,
                x,
                abajo + 52,
                color,
                14,
                anchor_x="center",
                anchor_y="bottom",
            )
