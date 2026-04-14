from typing import Optional
from .entidad import Entidad
from ..items.item import Item
from ..items.item import Equipamiento


class Personaje(Entidad):
    """Clase para el jugador controlable."""

    # Constantes de configuración de proyectiles
    COOLDOWN_BASE = 0.3  # segundos entre disparos
    # Límites superiores para upgrades
    MAX_DANO_PROYECTIL = 5.0  # 5x daño máximo
    MAX_VELOCIDAD_PROYECTIL = 3.0  # 3x velocidad máxima
    MIN_VELOCIDAD_DISPARO = 0.3  # 0.3x cooldown mínimo (disparos ~3x más rápidos)
    MAX_REBOTES = 5  # máximo 5 rebotes

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

        # ===== ATRIBUTOS DE MEJORA DE PROYECTILES =====
        # Multiplicador de velocidad de disparo (1.0 = normal, menor = más rápido)
        self._velocidad_disparo = 1.0
        # Multiplicador de daño de proyectil (1.0 = normal)
        self._dano_proyectil = 1.0
        # Multiplicador de velocidad del proyectil (1.0 = normal)
        self._velocidad_proyectil = 1.0
        # Cantidad de rebotes permitidos (0 = sin rebotes)
        self._rebotes = 0

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

    # ===== PROPIEDADES DE MEJORA DE PROYECTILES =====

    @property
    def velocidad_disparo(self) -> float:
        """Multiplicador de velocidad de disparo (1.0 = normal, menor = más rápido)."""
        return self._velocidad_disparo

    @property
    def dano_proyectil(self) -> float:
        """Multiplicador de daño de proyectil (1.0 = normal)."""
        return self._dano_proyectil

    @property
    def velocidad_proyectil(self) -> float:
        """Multiplicador de velocidad del proyectil (1.0 = normal)."""
        return self._velocidad_proyectil

    @property
    def rebotes(self) -> int:
        """Cantidad de rebotes permitidos (0 = sin rebotes)."""
        return self._rebotes

    @property
    def cooldown_disparo(self) -> float:
        """Tiempo de cooldown para el siguiente disparo."""
        return self.COOLDOWN_BASE * self._velocidad_disparo

    # ===== MÉTODOS DE MEJORA =====

    def mejorar_velocidad_disparo(self) -> None:
        """Reduce el cooldown de disparo en 15% (dispara más rápido)."""
        if self._velocidad_disparo > self.MIN_VELOCIDAD_DISPARO:
            self._velocidad_disparo = max(
                self.MIN_VELOCIDAD_DISPARO, self._velocidad_disparo * 0.85
            )

    def mejorar_dano_proyectil(self) -> None:
        """Aumenta el daño de proyectil en 25%."""
        if self._dano_proyectil < self.MAX_DANO_PROYECTIL:
            self._dano_proyectil = min(
                self.MAX_DANO_PROYECTIL, self._dano_proyectil * 1.25
            )

    def mejorar_velocidad_proyectil(self) -> None:
        """Aumenta la velocidad del proyectil en 20%."""
        if self._velocidad_proyectil < self.MAX_VELOCIDAD_PROYECTIL:
            self._velocidad_proyectil = min(
                self.MAX_VELOCIDAD_PROYECTIL, self._velocidad_proyectil * 1.20
            )

    def mejorar_rebote(self) -> None:
        """Agrega 1 rebote adicional."""
        if self._rebotes < self.MAX_REBOTES:
            self._rebotes += 1

    def reiniciar_upgrades(self) -> None:
        """Reinicia todos los upgrades de proyectil a valores base."""
        self._velocidad_disparo = 1.0
        self._dano_proyectil = 1.0
        self._velocidad_proyectil = 1.0
        self._rebotes = 0
