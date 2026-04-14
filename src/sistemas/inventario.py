from typing import Optional
from ..items.item import Item


class SistemaInventario:
    """Sistema para gestionar el inventario del personaje."""

    @staticmethod
    def agregar_item(inventario: list[Item], item: Item) -> None:
        """Agrega un item al inventario."""
        inventario.append(item)

    @staticmethod
    def usar_item(inventario: list[Item], indice: int, personaje) -> bool:
        """Usa un item del inventario por índice. Retorna True si se usó."""
        if 0 <= indice < len(inventario):
            item = inventario[indice]
            return item.usar(personaje)
        return False

    @staticmethod
    def vender_item(inventario: list[Item], indice: int, personaje) -> Optional[int]:
        """Vende un item del inventario. Retorna el oro obtenido o None."""
        if 0 <= indice < len(inventario):
            item = inventario.pop(indice)
            oro_obtenido = item.vender()
            personaje.agregar_oro(oro_obtenido)
            return oro_obtenido
        return None

    @staticmethod
    def comprar_item(inventario: list[Item], item: Item, personaje) -> bool:
        """Compra un item si el jugador tiene suficiente oro. Retorna True si se compró."""
        if item.precio <= personaje.oro:
            personaje.quitar_oro(item.precio)
            inventario.append(item)
            return True
        return False
