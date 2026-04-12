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
    ):
        super().__init__(hp_max, ataque, defensa)
        self._nombre = nombre
        self._tipo = tipo
        self._experiencia_al_derrotar = experiencia_al_derrotar
        self._oro_al_derrotar = oro_al_derrotar

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

    def esta_vivo(self) -> bool:
        return self._hp_actual > 0

    def __repr__(self) -> str:
        return f"Enemigo({self._nombre}, tipo={self._tipo}, hp={self._hp_actual}/{self._hp_max})"
