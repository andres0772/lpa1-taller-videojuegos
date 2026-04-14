from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import arcade
    from ..entidades.personaje import Personaje


class Item(ABC):
    """Clase base abstracta para todos los items del juego."""

    def __init__(self, nombre: str, descripcion: str = ""):
        self._nombre = nombre
        self._descripcion = descripcion
        # Sprite opcional asociado a este item (definido por la clase Juego)
        self.sprite: Optional[arcade.Sprite] = None

    def tiene_sprite(self) -> bool:
        """Retorna True si este item tiene un sprite asociado."""
        return self.sprite is not None

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @abstractmethod
    def usar(self, personaje: "Personaje") -> bool:
        """Intenta usar el item en un personaje. Retorna True si se usó."""
        pass


class Equipamiento(Item):
    """Clase para equipamiento (armas y armaduras)."""

    def __init__(
        self,
        nombre: str,
        tipo: str,  # "arma" o "armadura"
        bonus: int,
        precio: int = 0,
        descripcion: str = "",
    ):
        super().__init__(nombre, descripcion)
        self._tipo = tipo
        self._bonus = bonus
        self._precio = precio

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def bonus(self) -> int:
        return self._bonus

    @property
    def precio(self) -> int:
        return self._precio

    def usar(self, personaje: "Personaje") -> bool:
        """Equipa el objeto en el personaje."""
        if personaje.esta_vivo():
            personaje.equipar(self)
            return True
        return False

    def vender(self) -> int:
        """Vende el equipamiento. Retorna la mitad del precio."""
        return self._precio // 2


class Consumible(Item):
    """Clase para items consumibles (pociones, etc.)."""

    def __init__(
        self,
        nombre: str,
        efecto: int,  # Cantidad de HP a restaurar
        precio: int = 0,
        descripcion: str = "",
    ):
        super().__init__(nombre, descripcion)
        self._efecto = efecto
        self._precio = precio

    @property
    def efecto(self) -> int:
        return self._efecto

    @property
    def precio(self) -> int:
        return self._precio

    def usar(self, personaje: "Personaje") -> bool:
        """Consume el item y cura al personaje."""
        if personaje.esta_vivo():
            personaje.curar(self._efecto)
            return True
        return False

    def vender(self) -> int:
        """Vende el consumible. Retorna la mitad del precio."""
        return self._precio // 2


class Tesoro(Item):
    """Clase para tesoro (oro, experiencia, etc.)."""

    def __init__(
        self,
        nombre: str,
        valor: int,
        precio: int = 0,
        center_x: float = 0.0,
        center_y: float = 0.0,
    ):
        super().__init__(nombre, "")
        self._valor = valor
        self._precio = precio
        self.center_x = center_x
        self.center_y = center_y

    @property
    def valor(self) -> int:
        return self._valor

    @property
    def precio(self) -> int:
        return self._precio

    def usar(self, personaje: "Personaje") -> bool:
        """No se puede usar directamente, es para recolectar."""
        return False

    def vender(self) -> int:
        """Vende el tesoro. Retorna su valor."""
        return self._valor
