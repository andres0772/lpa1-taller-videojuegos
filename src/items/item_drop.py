"""ItemDrop - Items que dropping de enemigos derrotados."""

import random
from typing import TYPE_CHECKING, Optional

import arcade

from .item import Item

if TYPE_CHECKING:
    from ..entidades.personaje import Personaje


class ItemDrop(Item):
    """Items que dropping de enemigos derrotados.

    Probabilidades:
    - 50% tesoro (oro)
    - 20% trampa (daño)
    - 30% nada (ningún drop)
    """

    # Probabilidades de drop
    PROB_TESORO = 0.50
    PROB_TRAMPA = 0.20
    PROB_NADA = 0.30

    # Duración del drop en segundos
    DURACION_DROP = 5.0

    def __init__(
        self,
        center_x: float,
        center_y: float,
        tipo: str = "nada",
        valor: int = 0,
    ):
        """Crea un item drop.

        Args:
            center_x: Posición X del drop
            center_y: Posición Y del drop
            tipo: Tipo de drop ("tesoro", "trampa", "nada")
            valor: Valor del drop (oro o daño)
        """
        # Generar tipo y valor si no se especifica
        if tipo == "nada" and valor == 0:
            tipo, valor = self._generar_tipo_y_valor()

        nombre = f"Drop_{tipo}"
        super().__init__(nombre, f"Drop de tipo {tipo}")

        self._tipo = tipo
        self._valor = valor
        self.center_x = center_x
        self.center_y = center_y
        self._tiempo_existencia = 0.0

        # Sprite se crea después
        self.sprite: Optional[arcade.Sprite] = None

    @classmethod
    def _generar_tipo_y_valor(cls) -> tuple[str, int]:
        """Genera un tipo de drop y su valor según las probabilidades."""
        rand = random.random()
        if rand < cls.PROB_TESORO:
            # 50% tesoro - oro entre 10 y 50
            return ("tesoro", random.randint(10, 50))
        elif rand < cls.PROB_TESORO + cls.PROB_TRAMPA:
            # 20% trampa - daño entre 5 y 15
            return ("trampa", random.randint(5, 15))
        else:
            # 30% nada
            return ("nada", 0)

    @classmethod
    def crear_desde_enemigo(cls, enemigo) -> "ItemDrop | None":
        """Crea un ItemDrop desde la posición de un enemigo derrotado.

        Args:
            enemigo: El enemigo derrotado

        Returns:
            ItemDrop si hay drop, None si es "nada"
        """
        drop = cls(enemigo.center_x, enemigo.center_y)

        # Si el drop es "nada", no creamos nada
        if drop.tipo == "nada":
            return None

        return drop

    @property
    def tipo(self) -> str:
        """Retorna el tipo de drop."""
        return self._tipo

    @property
    def valor(self) -> int:
        """Retorna el valor del drop."""
        return self._valor

    @property
    def tiempo_existencia(self) -> float:
        """Retorna el tiempo que ha existido el drop."""
        return self._tiempo_existencia

    @property
    def expiro(self) -> bool:
        """Retorna True si el drop ha expirado."""
        return self._tiempo_existencia >= self.DURACION_DROP

    def actualizar_tiempo(self, delta_time: float) -> None:
        """Actualiza el tiempo de existencia del drop.

        Args:
            delta_time: Tiempo transcurrido desde el último update
        """
        self._tiempo_existencia += delta_time

    def crear_sprite(self) -> arcade.Sprite:
        """Crea el sprite visual del drop.

        Returns:
            Sprite del drop
        """
        if self._tipo == "tesoro":
            # Oro: cuadrado verde/amarillo
            sprite = arcade.SpriteSolidColor(20, 20, color=arcade.color.GOLD)
        elif self._tipo == "trampa":
            # Trampa: cuadrado rojo
            sprite = arcade.SpriteSolidColor(20, 20, color=arcade.color.RED)
        else:
            # Nada: cuadrado gris transparente
            sprite = arcade.SpriteSolidColor(20, 20, color=arcade.color.GRAY)

        sprite.center_x = self.center_x
        sprite.center_y = self.center_y
        self.sprite = sprite
        return sprite

    def usar(self, personaje: "Personaje") -> bool:
        """No se puede usar directamente - usar recoger()."""
        return False

    def recoger(self, personaje: "Personaje") -> tuple[str, int]:
        """Recoge el drop y aplica el efecto al personaje.

        Args:
            personaje: El personaje que recoge el drop

        Returns:
            Tupla (tipo, valor) del efecto aplicado
        """
        if self._tipo == "tesoro":
            personaje.agregar_oro(self._valor)
            return ("oro", self._valor)
        elif self._tipo == "trampa":
            personaje.recibir_daño(self._valor)
            return ("daño", self._valor)
        else:
            return ("nada", 0)

    def tiene_sprite(self) -> bool:
        """Retorna True si este drop tiene sprite asociado."""
        return self.sprite is not None
