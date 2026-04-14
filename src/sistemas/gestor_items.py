"""
Gestor de Items - Extraído de la clase Juego (God Class refactoring).

RESPONSABILIDAD ÚNICA (SRP): Este gestor se encarga exclusivamente de:
- Detectar colisiones con items (tesoros, trampas)
- Procesar recogida de items
- Aplicar efectos de items al personaje

PATRÓN APLICADO: Service Pattern - encapsula lógica de items
para reducir complejidad de la clase Juego principal.
"""

import arcade
from typing import TYPE_CHECKING, Callable

from ..entidades import Personaje
from ..items import Tesoro, TrampaExplosiva

if TYPE_CHECKING:
    from ..mundo.escenario import Escenario


class GestorItems:
    """Gestor con responsabilidad ÚNICA (SRP - Single Responsibility Principle)."""

    def __init__(self):
        """Inicializa el gestor de items."""
        pass

    def verificar_colisiones(
        self,
        personaje: Personaje,
        sprite_jugador: arcade.Sprite,
        items: list,
        lista_sprites: arcade.SpriteList,
        on_tesoro_recogido: Callable[[int], None] | None = None,
        on_trampa_activada: Callable[[int], None] | None = None,
    ) -> list:
        """
        Verifica colisiones con items y los procesa.

        Args:
            personaje: El personaje del jugador
            sprite_jugador: Sprite del jugador
            items: Lista de items en el escenario
            lista_sprites: Lista de sprites para poder eliminar
            on_tesoro_recogido: Callback cuando se recoge oro (recibe cantidad)
            on_trampa_activada: Callback cuando se activa una trampa (recibe daño)

        Returns:
            Lista de items procesados (ya eliminados del escenario)
        """
        items_procesados = []

        for item in list(items):  # list() para poder modificar
            if not item.tiene_sprite():
                continue

            if arcade.check_for_collision(sprite_jugador, item.sprite):
                # Procesar según el tipo de item
                if isinstance(item, Tesoro):
                    oro_ganado = item.valor
                    personaje.agregar_oro(oro_ganado)

                    if on_tesoro_recogido:
                        on_tesoro_recogido(oro_ganado)

                    # Eliminar sprite y item
                    if item.sprite in lista_sprites:
                        lista_sprites.remove(item.sprite)
                    items.remove(item)
                    items_procesados.append(item)

                elif isinstance(item, TrampaExplosiva):
                    daño = item.daño
                    item.activar(personaje)

                    if on_trampa_activada:
                        on_trampa_activada(daño)

                    # Eliminar sprite y item
                    if item.sprite in lista_sprites:
                        lista_sprites.remove(item.sprite)
                    items.remove(item)
                    items_procesados.append(item)

        return items_procesados

    def procesar_tesoro(
        self,
        personaje: Personaje,
        tesoro: Tesoro,
        items: list,
        lista_sprites: arcade.SpriteList,
    ) -> int:
        """
        Procesa la recogida de un tesoro.

        Args:
            personaje: El personaje que recoge el tesoro
            tesoro: El tesoro recogido
            items: Lista de items
            lista_sprites: Lista de sprites

        Returns:
            Cantidad de oro ganado
        """
        oro_ganado = tesoro.valor
        personaje.agregar_oro(oro_ganado)

        if tesoro.sprite in lista_sprites:
            lista_sprites.remove(tesoro.sprite)

        if tesoro in items:
            items.remove(tesoro)

        return oro_ganado

    def procesar_trampa(
        self,
        personaje: Personaje,
        trampa: TrampaExplosiva,
        items: list,
        lista_sprites: arcade.SpriteList,
    ) -> int:
        """
        Procesa la activación de una trampa.

        Args:
            personaje: El personaje que activa la trampa
            trampa: La trampa activada
            items: Lista de items
            lista_sprites: Lista de sprites

        Returns:
            Cantidad de daño recibido
        """
        daño = trampa.daño
        trampa.activar(personaje)

        if trampa.sprite in lista_sprites:
            lista_sprites.remove(trampa.sprite)

        if trampa in items:
            items.remove(trampa)

        return daño
