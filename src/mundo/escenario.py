"""Gestor de escenarios con múltiples áreas."""

from typing import Optional
from .area import Area


class Escenario:
    """Gestiona múltiples áreas/zonas del juego."""

    # Orden de las áreas disponibles
    AREAS_DISPONIBLES = ["bosque", "castillo", "campo"]

    def __init__(
        self, ancho: int = 1080, alto: int = 720, area_inicial: str = "bosque"
    ):
        self._ancho = ancho
        self._alto = alto
        self._areas: dict[str, Area] = {}
        self._area_actual: str = area_inicial

        # Crear todas las áreas
        self._crear_areas()

    def _crear_areas(self):
        """Crea todas las áreas del juego."""
        for tipo in self.AREAS_DISPONIBLES:
            self._areas[tipo] = Area(
                tipo, self._ancho, self._alto, generar_contenido=True
            )

    @property
    def ancho(self) -> int:
        return self._ancho

    @property
    def alto(self) -> int:
        return self._alto

    @property
    def area_actual(self) -> str:
        return self._area_actual

    @property
    def area(self) -> Area:
        """Retorna el área actual."""
        return self._areas[self._area_actual]

    @property
    def enemigos(self) -> list:
        """Retorna los enemigos del área actual."""
        return self.area.enemigos

    @property
    def items(self) -> list:
        """Retorna los items del área actual."""
        return self.area.items

    @property
    def nombre_area_actual(self) -> str:
        """Nombre legible del área actual."""
        return self.area.nombre

    @property
    def color_fondo(self) -> tuple:
        """Color de fondo del área actual."""
        return self.area.color_fondo

    @property
    def areas_disponibles(self) -> list[str]:
        """Lista de tipos de áreas disponibles."""
        return self.AREAS_DISPONIBLES

    def cambiar_area(self, tipo: str) -> bool:
        """Cambia al área especificada.

        Returns:
            True si el cambio fue exitoso, False si el área no existe.
        """
        if tipo in self._areas:
            self._area_actual = tipo
            return True
        return False

    def ir_area_siguiente(self) -> bool:
        """Avanza a la siguiente área en la lista circular."""
        indice_actual = self.AREAS_DISPONIBLES.index(self._area_actual)
        siguiente_indice = (indice_actual + 1) % len(self.AREAS_DISPONIBLES)
        self._area_actual = self.AREAS_DISPONIBLES[siguiente_indice]
        return True

    def ir_area_anterior(self) -> bool:
        """Retrocede a la área anterior en la lista circular."""
        indice_actual = self.AREAS_DISPONIBLES.index(self._area_actual)
        anterior_indice = (indice_actual - 1) % len(self.AREAS_DISPONIBLES)
        self._area_actual = self.AREAS_DISPONIBLES[anterior_indice]
        return True

    def agregar_enemigo(self, enemigo):
        """Agrega un enemigo al área actual."""
        self.area.agregar_enemigo(enemigo)

    def agregar_item(self, item):
        """Agrega un item al área actual."""
        self.area.agregar_item(item)

    def regenerar_contenido(self):
        """Regenera el contenido del área actual (enemies y items)."""
        self._areas[self._area_actual] = Area(
            self._area_actual, self._ancho, self._alto, generar_contenido=True
        )

    def __repr__(self) -> str:
        return f"Escenario(area={self._area_actual}, areas={len(self._areas)})"
