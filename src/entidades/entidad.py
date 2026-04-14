from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import arcade
    from .personaje import Personaje


class Entidad(ABC):
    """Clase abstracta base. Define el contrato que TODAS las entidades deben cumplir."""

    def __init__(self, hp_max: int, ataque: int, defensa: int):
        self._hp_max = hp_max
        self._hp_actual = hp_max
        self._ataque = ataque
        self._defensa = defensa
        # Sprite opcional asociado a esta entidad (definido por la clase Juego)
        self.sprite: Optional[arcade.Sprite] = None

    def tiene_sprite(self) -> bool:
        """Retorna True si esta entidad tiene un sprite asociado."""
        return self.sprite is not None

    # Properties para encapsulamiento
    @property
    def hp_max(self) -> int:
        return self._hp_max

    @property
    def hp_actual(self) -> int:
        return self._hp_actual

    @property
    def ataque(self) -> int:
        return self._ataque

    @property
    def defensa(self) -> int:
        return self._defensa

    @property
    def ataque_total(self) -> int:
        """Retorna el ataque total. Por defecto igual a ataque base.
        Las subclases pueden sobrescribir para agregar modificadores."""
        return self._ataque

    @property
    def defensa_total(self) -> int:
        """Retorna la defensa total. Por defecto igual a defensa base.
        Las subclases pueden sobrescribir para agregar modificadores."""
        return self._defensa

    @abstractmethod
    def esta_vivo(self) -> bool:
        """Retorna True si la entidad tiene HP > 0. Las subclases DEBEN implementar (polimorfismo)."""
        pass

    @abstractmethod
    def puede_recibir_daño(self) -> bool:
        """Retorna True si puede recibir daño. Las subclases DEBEN implementar (polimorfismo)."""
        pass

    @abstractmethod
    def puede_ser_destruido(self) -> bool:
        """Retorna True si debe eliminarse. Las subclases DEBEN implementar (polimorfismo)."""
        pass

    def recibir_daño(self, daño: int) -> None:
        """Reduce el HP actual por el daño recibido (ya calculado por el sistema de combate)."""
        self._hp_actual = max(0, self._hp_actual - daño)

    def curar(self, cantidad: int) -> None:
        """Incrementa el HP actual sin superar el HP máximo."""
        self._hp_actual = min(self._hp_max, self._hp_actual + cantidad)
