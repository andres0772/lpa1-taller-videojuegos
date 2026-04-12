from typing import Optional
import random
from ..entidades.enemigo import Enemigo
from ..items.item import Item


class Escenario:
    """Gestiona el mapa/escenario del juego."""

    def __init__(self, ancho: int = 1080, alto: int = 720):
        self._ancho = ancho
        self._alto = alto
        self._enemigos: list[Enemigo] = []
        self._items: list[Item] = []

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

    def agregar_enemigo(self, enemigo: Enemigo) -> None:
        """Agrega un enemigo al escenario."""
        self._enemigos.append(enemigo)

    def agregar_item(self, item: Item) -> None:
        """Agrega un item al escenario."""
        self._items.append(item)

    def generar_enemigos_aleatorios(self, cantidad: int = 5) -> None:
        """Genera enemigos aleatorios en el escenario."""
        tipos = ["terrestre", "volador"]
        nombres = {
            "terrestre": ["Goblin", "Orco", "Slime", "Zombie"],
            "volador": ["Murciélago", "Gárgola", "Dragón pequeño"],
        }

        for _ in range(cantidad):
            tipo = random.choice(tipos)
            nombre = random.choice(nombres[tipo])
            hp = random.randint(20, 50)
            ataque = random.randint(5, 15)
            defensa = random.randint(0, 5)
            xp = random.randint(10, 30)
            oro = random.randint(5, 20)

            enemigo = Enemigo(nombre, hp, ataque, defensa, tipo, xp, oro)
            # Posición aleatoria
            enemigo.center_x = random.randint(50, self._ancho - 50)
            enemigo.center_y = random.randint(50, self._alto - 50)
            self.agregar_enemigo(enemigo)

    def generar_items_aleatorios(self, cantidad: int = 3) -> None:
        """Genera items aleatorios (tesoros) en el escenario."""
        from ..items.item import Tesoro

        for _ in range(cantidad):
            valor = random.randint(10, 100)
            tesoro = Tesoro(f"Oro {valor}", valor)
            tesoro.center_x = random.randint(50, self._ancho - 50)
            tesoro.center_y = random.randint(50, self._alto - 50)
            self.agregar_item(tesoro)

    def __repr__(self) -> str:
        return f"Escenario(enemigos={len(self._enemigos)}, items={len(self._items)})"
