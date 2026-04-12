"""Sistema de áreas/zonas del juego."""

import random
from typing import Optional
from ..entidades.enemigo import Enemigo
from ..items.item import Item


class Area:
    """Representa una zona/área del juego con sus propios enemigos y items."""

    # Tipos de áreas predefinidas
    TIPOS = {
        "bosque": {
            "color_fondo": (34, 139, 34),  # Forest Green
            "nombre": "Bosque Encantado",
            "descripcion": "Un bosque misterioso con criaturas salvajes",
            "enemigos_tipo": ["terrestre", "volador"],
            "enemigos_nombres": {
                "terrestre": ["Goblin", "Orco", "Slime", "Zombie"],
                "volador": ["Murciélago", "Gárgola"],
            },
        },
        "castillo": {
            "color_fondo": (80, 80, 80),  # Dark Gray
            "nombre": "Castillo Oscuro",
            "descripcion": "Las ruinas de un antiguo castillo embrujado",
            "enemigos_tipo": ["terrestre", "volador"],
            "enemigos_nombres": {
                "terrestre": ["Esqueleto", "Caballero Oscuro", "Golem"],
                "volador": ["Murciélago Gigante", "Demonio Volador"],
            },
        },
        "campo": {
            "color_fondo": (107, 142, 35),  # Olive Drab
            "nombre": "Campo de Batalla",
            "descripcion": "Campos abiertos donde guerreros cayeron en batalla",
            "enemigos_tipo": ["terrestre"],
            "enemigos_nombres": {
                "terrestre": ["Bandido", "Mercenario", "Caballo de Guerra"],
            },
        },
    }

    def __init__(
        self,
        tipo: str = "bosque",
        ancho: int = 1080,
        alto: int = 720,
        generar_contenido: bool = True,
        nivel: int = 1,
    ):
        self._tipo = tipo
        self._ancho = ancho
        self._alto = alto
        self._nivel = nivel  # Nivel de dificultad progresiva
        self._enemigos: list[Enemigo] = []
        self._items: list[Item] = []

        # Obtener configuración del tipo de área
        self._config = self.TIPOS.get(tipo, self.TIPOS["bosque"])

        if generar_contenido:
            self._generar_contenido()

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def nombre(self) -> str:
        return self._config["nombre"]

    @property
    def descripcion(self) -> str:
        return self._config["descripcion"]

    @property
    def color_fondo(self) -> tuple:
        return self._config["color_fondo"]

    @property
    def ancho(self) -> int:
        return self._ancho

    @property
    def alto(self) -> int:
        return self._alto

    @property
    def enemigos(self) -> list[Enemigo]:
        return self._enemigos

    @property
    def items(self) -> list[Item]:
        return self._items

    def _generar_contenido(self):
        """Genera enemigos y items aleatorios para el área."""
        self._generar_enemigos()
        self._generar_items()

    def _generar_enemigos(self, cantidad: int = 5):
        """Genera enemigos aleatorios según el tipo de área."""
        tipos = self._config["enemigos_tipo"]
        nombres = self._config["enemigos_nombres"]

        # R7.2: Agregar jefe en el área 3 (Castillo Oscuro)
        generar_jefe = self._tipo == "castillo"

        # Multiplicadores según el nivel del juego
        multiplicador_hp = 1.0 + (self._nivel - 1) * 0.3  # +30% HP por nivel
        multiplicador_ataque = 1.0 + (self._nivel - 1) * 0.2  # +20% ataque por nivel

        for i in range(cantidad):
            tipo = random.choice(tipos)
            nombre = random.choice(nombres.get(tipo, ["Criatura"]))
            hp = int(random.randint(20, 50) * multiplicador_hp)
            ataque = int(random.randint(5, 15) * multiplicador_ataque)
            defensa = int(random.randint(0, 5) * multiplicador_hp)
            xp = int(random.randint(10, 30) * multiplicador_hp)
            oro = int(random.randint(5, 20) * multiplicador_hp)
            es_jefe = False

            # El primer enemigo del castillo es el jefe
            if generar_jefe and i == 0:
                nombre = "Señor Oscuro"
                hp = int(200 * multiplicador_hp)  # Más HP que un enemigo normal
                ataque = int(25 * multiplicador_ataque)  # Más ataque
                defensa = int(15 * multiplicador_hp)
                xp = int(500 * multiplicador_hp)  # Mucha XP
                oro = int(300 * multiplicador_hp)
                es_jefe = True

            enemigo = Enemigo(nombre, hp, ataque, defensa, tipo, xp, oro, es_jefe)
            enemigo.center_x = random.randint(50, self._ancho - 50)
            enemigo.center_y = random.randint(50, self._alto - 50)
            self._enemigos.append(enemigo)

    def _generar_items(self, cantidad: int = 3):
        """Genera items aleatorios (tesoros) en el área."""
        from ..items.item import Tesoro

        for _ in range(cantidad):
            valor = random.randint(10, 100)
            tesoro = Tesoro(f"Oro {valor}", valor)
            tesoro.center_x = random.randint(50, self._ancho - 50)
            tesoro.center_y = random.randint(50, self._alto - 50)
            self._items.append(tesoro)

    def agregar_enemigo(self, enemigo: Enemigo):
        """Agrega un enemigo al área."""
        self._enemigos.append(enemigo)

    def agregar_item(self, item: Item):
        """Agrega un item al área."""
        self._items.append(item)

    def __repr__(self) -> str:
        return f"Area({self.nombre}, enemigos={len(self._enemigos)}, items={len(self._items)})"
