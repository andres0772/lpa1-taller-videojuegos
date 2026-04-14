"""
Gestor de Combate Cuerpo a Cuerpo - Extraído de la clase Juego (God Class refactoring).

RESPONSABILIDAD ÚNICA (SRP): Este gestor se encarga exclusivamente de:
- Detectar colisiones con enemigos
- Ejecutar combate cuerpo a cuerpo
- Gestionar cooldowns de combate
- Procesar derrotas de enemigos

PATRÓN APLICADO: Service Pattern - encapsula lógica de combate
para reducir complejidad de la clase Juego principal.
"""

import arcade
from typing import TYPE_CHECKING, Callable

from ..entidades import Personaje, Enemigo
from ..sistemas import SistemaCombate, ResultadoCombate

if TYPE_CHECKING:
    from ..mundo.escenario import Escenario


class GestorCombate:
    """Gestor con responsabilidad ÚNICA (SRP - Single Responsibility Principle)."""

    # Constantes de configuración
    COOLDOWN_COMBATE = 1.0  # segundos entre combates

    def __init__(self):
        """Inicializa el gestor de combate."""
        self._cooldown = 0.0

    @property
    def puede_combatir(self) -> bool:
        """Retorna True si el jugador puede combatir (cooldown expirado)."""
        return self._cooldown <= 0

    def actualizar_cooldown(self, delta_time: float) -> None:
        """Actualiza el cooldown de combate."""
        self._cooldown = max(0, self._cooldown - delta_time)

    def verificar_combate(
        self,
        personaje: Personaje,
        sprite_jugador: arcade.Sprite,
        enemigos: list[Enemigo],
        lista_sprites: arcade.SpriteList,
        on_enemigo_derrotado: Callable[[Enemigo], None] | None = None,
        on_jefe_derrotado: Callable[[], None] | None = None,
    ) -> ResultadoCombate | None:
        """
        Verifica si hay colisión con enemigos y ejecuta combate.

        Args:
            personaje: El personaje del jugador
            sprite_jugador: Sprite del jugador
            enemigos: Lista de enemigos en el escenario
            lista_sprites: Lista de sprites para poder eliminar
            on_enemigo_derrotado: Callback cuando un enemigo es derrotado
            on_jefe_derrotado: Callback cuando un jefe es derrotado

        Returns:
            ResultadoCombate si hubo combate, None si no hubo
        """
        if not self.puede_combatir:
            return None

        for enemigo in list(enemigos):  # list() para poder modificar
            if not enemigo.esta_vivo():
                continue

            if not enemigo.tiene_sprite():
                continue

            if arcade.check_for_collision(sprite_jugador, enemigo.sprite):
                # ¡Combate!
                resultado = SistemaCombate.atacar(personaje, enemigo)

                # Activar cooldown
                self._cooldown = self.COOLDOWN_COMBATE

                # Procesar derrota del enemigo
                if resultado.enemigo_derrotado:
                    # Ganar experiencia y oro
                    personaje.ganar_experiencia(enemigo.experiencia_al_derrotar)
                    personaje.agregar_oro(enemigo.oro_al_derrotar)

                    # Callback de enemigo derrotado
                    if on_enemigo_derrotado:
                        on_enemigo_derrotado(enemigo)

                    # Eliminar sprite
                    if enemigo.sprite in lista_sprites:
                        lista_sprites.remove(enemigo.sprite)

                    # Verificar si era jefe
                    if enemigo.es_jefe and on_jefe_derrotado:
                        on_jefe_derrotado()

                    # Eliminar enemigo de la lista
                    enemigos.remove(enemigo)

                return resultado

        return None

    def procesar_derrota_enemigo(
        self,
        personaje: Personaje,
        enemigo: Enemigo,
        enemigos: list[Enemigo],
        lista_sprites: arcade.SpriteList,
    ) -> bool:
        """
        Procesa la derrota de un enemigo.

        Args:
            personaje: El personaje que derrotó al enemigo
            enemigo: El enemigo derrotado
            enemigos: Lista de enemigos
            lista_sprites: Lista de sprites

        Returns:
            True si el enemigo era un jefe
        """
        personaje.ganar_experiencia(enemigo.experiencia_al_derrotar)
        personaje.agregar_oro(enemigo.oro_al_derrotar)

        if enemigo.sprite in lista_sprites:
            lista_sprites.remove(enemigo.sprite)

        if enemigo in enemigos:
            enemigos.remove(enemigo)

        return enemigo.es_jefe
