from typing import Literal
from .entidad import Entidad


class Proyectil(Entidad):
    """Hereda de Entidad. Ejemplo de HERENCIA - reutiliza código de la clase base."""

    # HP fijo para proyectiles (se destruyen con cualquier impacto)
    HP_PROYECTIL = 1

    def __init__(
        self,
        x: float,
        y: float,
        direccion_x: float,
        direccion_y: float,
        dano: int,
        velocidad: float = 300,
        es_del_jugador: bool = True,
    ):
        # Inicializar como Entidad con HP=1 (los proyectiles se destruyen con 1 golpe)
        super().__init__(hp_max=self.HP_PROYECTIL, ataque=dano, defensa=0)

        self.center_x = x
        self.center_y = y
        self.direccion_x = direccion_x
        self.direccion_y = direccion_y
        self._dano = dano  # Daño que inflige al impactar
        self.velocidad = velocidad
        self.es_del_jugador = es_del_jugador
        self.sprite = None
        self.activo = True

    @property
    def dano(self) -> int:
        """Daño que inflige el proyectil al impactar."""
        return self._dano

    @property
    def posicion(self) -> tuple[float, float]:
        return (self.center_x, self.center_y)

    @property
    def direccion(self) -> tuple[float, float]:
        return (self.direccion_x, self.direccion_y)

    @property
    def color(self) -> tuple[int, int, int]:
        """Retorna el color del proyectil según quién lo disparó."""
        if self.es_del_jugador:
            return (0, 255, 255)  # Cyan para el jugador
        else:
            return (255, 165, 0)  # Naranja para enemigos

    @property
    def tamaño(self) -> int:
        """Retorna el tamaño del proyectil."""
        return 10

    # Implementación de métodos abstractos de Entidad (polimorfismo)
    def esta_vivo(self) -> bool:
        """Un proyectil está 'vivo' mientras esté activo. Implementa método de Entidad (polimorfismo)."""
        return self.activo and self._hp_actual > 0

    def puede_recibir_daño(self) -> bool:
        """Implementa método de Entidad (polimorfismo)."""
        return self.activo

    def puede_ser_destruido(self) -> bool:
        """Implementa método de Entidad (polimorfismo)."""
        return not self.activo or self._hp_actual <= 0

    def esta_fuera_de_pantalla(self, ancho: int, alto: int) -> bool:
        """Verifica si el proyectil salió de la pantalla."""
        return (
            self.center_x < 0
            or self.center_x > ancho
            or self.center_y < 0
            or self.center_y > alto
        )

    def actualizar(self, delta_time: float) -> None:
        """Actualiza la posición del proyectil."""
        if not self.activo:
            return

        desplazamiento = self.velocidad * delta_time
        self.center_x += self.direccion_x * desplazamiento
        self.center_y += self.direccion_y * desplazamiento

    def __repr__(self) -> str:
        tipo = "jugador" if self.es_del_jugador else "enemigo"
        return f"Proyectil({tipo}, dano={self._dano}, pos={self.center_x:.0f},{self.center_y:.0f})"
