from .item import Item


class TrampaExplosiva(Item):
    """Trampa que causa daño en área."""

    def __init__(self, nombre: str, daño: int, alcance: int):
        super().__init__(nombre, "Trampa explosiva")
        self._daño = daño
        self._alcance = alcance

    @property
    def daño(self) -> int:
        return self._daño

    @property
    def alcance(self) -> int:
        return self._alcance

    def usar(self, personaje) -> bool:
        """Las trampas no se usan directamente, se activan al contacto."""
        return False

    def activar(self, entidad) -> None:
        """Activa la trampa contra una entidad."""
        entidad.recibir_daño(self._daño)
