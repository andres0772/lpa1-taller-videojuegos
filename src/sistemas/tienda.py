"""Sistema de tienda del juego."""

from typing import Optional
from ..items.item import Equipamiento


class ItemTienda:
    """Representa un item disponible para comprar en la tienda."""

    def __init__(self, equipamiento: Equipamiento, stock: int = 999):
        self.equipamiento = equipamiento
        self.stock = stock  # Cantidad disponible (-1 = ilimitado)

    @property
    def nombre(self) -> str:
        return self.equipamiento.nombre

    @property
    def precio(self) -> int:
        return self.equipamiento.precio

    @property
    def tipo(self) -> str:
        return self.equipamiento.tipo

    @property
    def bonus(self) -> int:
        return self.equipamiento.bonus


class SistemaTienda:
    """Sistema para gestionar la tienda del juego."""

    # Items disponibles en la tienda
    ITEMS_TIENDA = [
        # Armas básicas
        ItemTienda(
            Equipamiento(
                "Espada Básica",
                "arma",
                5,
                precio=50,
                descripcion="Espada simple de entrenamiento",
            ),
            stock=5,
        ),
        ItemTienda(
            Equipamiento(
                "Escudo Básico",
                "armadura",
                3,
                precio=30,
                descripcion="Escudo de madera",
            ),
            stock=5,
        ),
        # Armas avanzadas
        ItemTienda(
            Equipamiento(
                "Espada Avanzada",
                "arma",
                10,
                precio=150,
                descripcion="Espada de acero templado",
            ),
            stock=2,
        ),
        ItemTienda(
            Equipamiento(
                "Armadura Mejorada",
                "armadura",
                8,
                precio=100,
                descripcion="Armadura de cuero endurecido",
            ),
            stock=2,
        ),
    ]

    @classmethod
    def getter_items_tienda(cls) -> list[ItemTienda]:
        """Retorna la lista de items disponibles en la tienda."""
        return cls.ITEMS_TIENDA

    @classmethod
    def comprar_item(cls, indice: int, personaje) -> tuple[bool, str]:
        """Compra un item de la tienda.

        Retorna (éxito, mensaje).
        """
        if indice < 0 or indice >= len(cls.ITEMS_TIENDA):
            return False, "Item no válido"

        item_tienda = cls.ITEMS_TIENDA[indice]

        if item_tienda.stock <= 0:
            return False, "No hay stock disponible"

        if personaje.oro < item_tienda.precio:
            return (
                False,
                f"Oro insuficiente (tienes {personaje.oro}, necesitas {item_tienda.precio})",
            )

        # Descontar oro y crear copia del equipamiento
        personaje.quitar_oro(item_tienda.precio)

        # Crear una copia del equipamiento para el inventario
        equip = Equipamiento(
            item_tienda.nombre,
            item_tienda.tipo,
            item_tienda.bonus,
            precio=item_tienda.precio,
            descripcion=item_tienda.equipamiento.descripcion,
        )

        # Agregar al inventario
        personaje._inventario.append(equip)

        # Descontar stock (si hay límite)
        if item_tienda.stock > 0:
            item_tienda.stock -= 1

        return True, f"¡Compraste {item_tienda.nombre} por {item_tienda.precio} oro!"

    @classmethod
    def vender_item(cls, indice: int, personaje) -> tuple[bool, str]:
        """Vende un item del inventario.

        Retorna (éxito, mensaje).
        """
        if indice < 0 or indice >= len(personaje.inventario):
            return False, "Índice de item no válido"

        if not personaje.inventario:
            return False, "El inventario está vacío"

        item = personaje.inventario[indice]

        # Verificar que sea un equipamiento vendible
        from ..items.item import Equipamiento

        if not isinstance(item, Equipamiento):
            return False, "Solo se pueden vender equipamiento"

        # Obtener valor de venta
        oro_venta = item.vender()

        # Remover del inventario
        personaje.inventario.pop(indice)

        # Agregar oro
        personaje.agregar_oro(oro_venta)

        return True, f"¡Vendiste {item.nombre} por {oro_venta} oro!"
