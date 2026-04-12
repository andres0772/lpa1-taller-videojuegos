from typing import Literal
from .item import Item


class Equipamiento(Item):
    """Equipo que mejora stats del personaje."""

    def __init__(
        self, nombre: str, tipo: Literal["arma", "armadura"], bonus: int, precio: int
    ):
        super().__init__(nombre, "Equipamiento")
        self._tipo = tipo
        self._bonus = bonus
        self._precio = precio

    @property
    def tipo(self) -> Literal["arma", "armadura"]:
        return self._tipo

    @property
    def bonus(self) -> int:
        return self._bonus

    @property
    def precio(self) -> int:
        return self._precio

    def usar(self, personaje) -> bool:
        """Se equipa automáticamente."""
        personaje.equipar(self)
        return True

    def vender(self) -> int:
        return self._precio // 2
