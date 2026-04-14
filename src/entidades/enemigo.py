from typing import Literal
from .entidad import Entidad


class Enemigo(Entidad):
    """Clase para los enemigos del juego."""

    def __init__(
        self,
        nombre: str,
        hp_max: int,
        ataque: int,
        defensa: int,
        tipo: Literal["terrestre", "volador"],
        experiencia_al_derrotar: int = 10,
        oro_al_derrotar: int = 5,
        es_jefe: bool = False,
    ):
        super().__init__(hp_max, ataque, defensa)
        self._nombre = nombre
        self._tipo = tipo
        self._experiencia_al_derrotar = experiencia_al_derrotar
        self._oro_al_derrotar = oro_al_derrotar
        self._es_jefe = es_jefe  # Flag para identificar bosses
        # Posición en el escenario
        self.center_x: float = 0.0
        self.center_y: float = 0.0

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tipo(self) -> Literal["terrestre", "volador"]:
        return self._tipo

    @property
    def experiencia_al_derrotar(self) -> int:
        return self._experiencia_al_derrotar

    @property
    def oro_al_derrotar(self) -> int:
        return self._oro_al_derrotar

    @property
    def es_jefe(self) -> bool:
        """Retorna True si este enemigo es un jefe."""
        return self._es_jefe

    def puede_recibir_daño(self) -> bool:
        """Retorna True si puede recibir daño (solo si está vivo)."""
        return self.esta_vivo()

    def puede_ser_destruido(self) -> bool:
        """Retorna True si debe ser eliminado (solo si HP <= 0)."""
        return self.hp_actual <= 0

    def esta_vivo(self) -> bool:
        return self._hp_actual > 0

    def __repr__(self) -> str:
        return f"Enemigo({self._nombre}, tipo={self._tipo}, hp={self._hp_actual}/{self._hp_max})"
