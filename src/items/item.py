from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entidades.personaje import Personaje


class Item(ABC):
    """Clase base abstracta para todos los items del juego."""

    def __init__(self, nombre: str, descripcion: str = ""):
        self._nombre = nombre
        self._descripcion = descripcion

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
        descripcion: str = "",
    ):
        super().__init__(nombre, descripcion)
        self._tipo = tipo
        self._bonus = bonus

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def bonus(self) -> int:
        return self._bonus

    def usar(self, personaje: "Personaje") -> bool:
        """Equipa el objeto en el personaje."""
        personaje.equipar(self)
        return True


class Consumible(Item):
    """Clase para items consumibles (pociones, etc.)."""

    def __init__(
        self,
        nombre: str,
        efecto: int,  # Cantidad de HP a restaurar
        descripcion: str = "",
    ):
        super().__init__(nombre, descripcion)
        self._efecto = efecto

    @property
    def efecto(self) -> int:
        return self._efecto

    def usar(self, personaje: "Personaje") -> bool:
        """Consume el item y cura al personaje."""
        if personaje.esta_vivo():
            personaje.curar(self._efecto)
            return True
        return False


class Tesoro(Item):
    """Clase para tesoro (oro, experiencia, etc.)."""

    def __init__(self, nombre: str, valor: int):
        super().__init__(nombre, "")
        self._valor = valor

    @property
    def valor(self) -> int:
        return self._valor

    def usar(self, personaje: "Personaje") -> bool:
        """No se puede usar directamente, es para recolectar."""
        return False
