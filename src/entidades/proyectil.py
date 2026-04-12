from typing import Literal


class Proyectil:
    """Clase para los proyectiles disparados en el juego."""

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
        self.center_x = x
        self.center_y = y
        self.direccion_x = direccion_x
        self.direccion_y = direccion_y
        self.dano = dano
        self.velocidad = velocidad
        self.es_del_jugador = es_del_jugador
        self.sprite = None
        self.activo = True

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
        return f"Proyectil({tipo}, dano={self.dano}, pos={self.center_x:.0f},{self.center_y:.0f})"
