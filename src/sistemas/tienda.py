"""Sistema de tienda del juego."""

from typing import Optional, Union
from ..items.item import Equipamiento, MejoraProyectil


class ItemTienda:
    """Representa un item disponible para comprar en la tienda."""

    def __init__(
        self,
        item: Union[Equipamiento, MejoraProyectil],
        stock: int = 999,
    ):
        self.item = item
        self.stock = stock  # Cantidad disponible (-1 = ilimitado)

    @property
    def nombre(self) -> str:
        return self.item.nombre

    @property
    def precio(self) -> int:
        return self.item.precio

    @property
    def tipo(self) -> str:
        return self.item.tipo

    @property
    def bonus(self) -> int:
        if isinstance(self.item, Equipamiento):
            return self.item.bonus
        return 0


class SistemaTienda:
    """Sistema para gestionar la tienda del juego."""

    # Items disponibles en la tienda (MEJORAS DE PROYECTILES)
    ITEMS_TIENDA = [
        # Mejoras de proyectiles
        ItemTienda(
            MejoraProyectil(
                "Velocidad de disparo",
                MejoraProyectil.TIPO_VELOCIDAD_DISPARO,
                precio=50,
                descripcion="Reduce el cooldown de disparo un 15%",
            ),
            stock=-1,  # Ilimitado
        ),
        ItemTienda(
            MejoraProyectil(
                "Daño de proyectil",
                MejoraProyectil.TIPO_DANO_PROYECTIL,
                precio=75,
                descripcion="Aumenta el daño de proyectil un 25%",
            ),
            stock=-1,
        ),
        ItemTienda(
            MejoraProyectil(
                "Velocidad de proyectil",
                MejoraProyectil.TIPO_VELOCIDAD_PROYECTIL,
                precio=60,
                descripcion="Aumenta la velocidad del proyectil un 20%",
            ),
            stock=-1,
        ),
        ItemTienda(
            MejoraProyectil(
                "Rebote",
                MejoraProyectil.TIPO_REBOTE,
                precio=100,
                descripcion="Agrega 1 rebote adicional",
            ),
            stock=-1,
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

        if item_tienda.stock == 0:
            return False, "No hay stock disponible"

        if personaje.oro < item_tienda.precio:
            return (
                False,
                f"Oro insuficiente (tienes {personaje.oro}, necesitas {item_tienda.precio})",
            )

        # Descontar oro
        personaje.quitar_oro(item_tienda.precio)

        # Usar la mejora directamente (aplica el efecto)
        item_tienda.item.usar(personaje)

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
