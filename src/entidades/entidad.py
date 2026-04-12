from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .personaje import Personaje


class Entidad(ABC):
    """Clase base abstracta para todas las entidades del juego."""

    def __init__(self, hp_max: int, ataque: int, defensa: int):
        self._hp_max = hp_max
        self._hp_actual = hp_max
        self._ataque = ataque
        self._defensa = defensa

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

    @abstractmethod
    def esta_vivo(self) -> bool:
        """Retorna True si la entidad tiene HP > 0."""
        pass

    def recibir_daño(self, daño: int) -> None:
        """Reduce el HP actual por el daño recibido (ya calculado por el sistema de combate)."""
        self._hp_actual = max(0, self._hp_actual - daño)

    def curar(self, cantidad: int) -> None:
        """Incrementa el HP actual sin superar el HP máximo."""
        self._hp_actual = min(self._hp_max, self._hp_actual + cantidad)
