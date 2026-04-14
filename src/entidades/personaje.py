from typing import Optional
from .entidad import Entidad
from ..items.item import Item
from ..items.item import Equipamiento


class Personaje(Entidad):
    """Clase para el jugador controlable."""

    def __init__(self, nombre: str = "Heroe"):
        # Stats base para nivel 1
        super().__init__(hp_max=100, ataque=10, defensa=5)
        self._nombre = nombre
        self._nivel = 1
        self._experiencia = 0
        self._experiencia_siguiente_nivel = 100
        self._oro = 0
        self._inventario: list[Item] = []
        self._arma_equipada: Optional[Equipamiento] = None
        self._armadura_equipada: Optional[Equipamiento] = None

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def nivel(self) -> int:
        return self._nivel

    @property
    def experiencia(self) -> int:
        return self._experiencia

    @property
    def experiencia_siguiente_nivel(self) -> int:
        return self._experiencia_siguiente_nivel

    @property
    def oro(self) -> int:
        return self._oro

    def agregar_oro(self, cantidad: int) -> None:
        """Método público para modificar _oro (ENCAPSULAMIENTO - no acceso directo)."""
        if cantidad > 0:
            self._oro += cantidad

    def quitar_oro(self, cantidad: int) -> None:
        """Método público para modificar _oro (ENCAPSULAMIENTO - no acceso directo)."""
        if cantidad > 0 and self._oro >= cantidad:
            self._oro -= cantidad

    @property
    def inventario(self) -> list[Item]:
        return self._inventario

    @property
    def arma_equipada(self) -> Optional[Equipamiento]:
        return self._arma_equipada

    @property
    def armadura_equipada(self) -> Optional[Equipamiento]:
        return self._armadura_equipada

    def puede_recibir_daño(self) -> bool:
        """Retorna True si puede recibir daño (solo si está vivo)."""
        return self.esta_vivo()

    def puede_ser_destruido(self) -> bool:
        """Retorna True si debe ser eliminado (solo si HP <= 0)."""
        return self.hp_actual <= 0

    def esta_vivo(self) -> bool:
        return self._hp_actual > 0

    def ganar_experiencia(self, xp: int) -> None:
        """Agrega experiencia y verifica level up."""
        self._experiencia += xp
        while self._experiencia >= self._experiencia_siguiente_nivel:
            self._subir_nivel()

    def _subir_nivel(self) -> None:
        """Sube de nivel aumentando stats."""
        self._nivel += 1
        self._experiencia -= self._experiencia_siguiente_nivel
        self._experiencia_siguiente_nivel = int(self._experiencia_siguiente_nivel * 1.5)
        # Mejora de stats
        self._hp_max += 20
        self._hp_actual = self._hp_max  # Curar al subir nivel
        self._ataque += 5
        self._defensa += 3

    def agregar_item(self, item: Item) -> None:
        """Agrega un item al inventario."""
        self._inventario.append(item)

    def usar_item(self, item: Item) -> bool:
        """Intenta usar un item. Retorna True si se usó."""
        return item.usar(self)

    def equipar(self, equipamiento: Equipamiento) -> None:
        """Equipa un objeto en la ranura correspondiente."""
        if equipamiento.tipo == "arma":
            self._arma_equipada = equipamiento
        elif equipamiento.tipo == "armadura":
            self._armadura_equipada = equipamiento

    @property
    def ataque_total(self) -> int:
        """Retorna ataque total incluyendo equipamiento."""
        bonus = 0
        if self._arma_equipada:
            bonus += self._arma_equipada.bonus
        return self._ataque + bonus

    @property
    def defensa_total(self) -> int:
        """Retorna defensa total incluyendo equipamiento."""
        bonus = 0
        if self._armadura_equipada:
            bonus += self._armadura_equipada.bonus
        return self._defensa + bonus
