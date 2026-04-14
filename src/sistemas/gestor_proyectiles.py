"""
Gestor de Proyectiles - Extraído de la clase Juego (God Class refactoring).

RESPONSABILIDAD ÚNICA (SRP): Este gestor se encarga exclusivamente de:
- Crear proyectiles del jugador
- Crear proyectiles de enemigos
- Actualizar posiciones de proyectiles
- Detectar colisiones con enemigos/jugador
- Eliminar proyectiles inactivos

PATRÓN APLICADO: Service Pattern - encapsula lógica de proyectiles
para reducir complejidad de la clase Juego principal.
"""

import random
import arcade
from typing import TYPE_CHECKING

from ..entidades import Proyectil, Enemigo, Personaje

if TYPE_CHECKING:
    from ..mundo.escenario import Escenario


class GestorProyectiles:
    """Gestor con responsabilidad ÚNICA (SRP - Single Responsibility Principle)."""

    # Constantes de configuración
    VELOCIDAD_PROYECTIL_JUGADOR = 400  # pixels por segundo
    VELOCIDAD_PROYECTIL_ENEMIGO = 280  # 70% de la velocidad del jugador
    DANO_PROYECTIL_JUGADOR = 10  # Reducido de 15 para permitir múltiples impactos
    DANO_PROYECTIL_ENEMIGO = 8
    COOLDOWN_DISPARO_JUGADOR = 0.3  # segundos
    COOLDOWN_MIN_ENEMIGO = 2.0  # segundos
    COOLDOWN_MAX_ENEMIGO = 5.0  # segundos

    def __init__(self, ancho_pantalla: int, alto_pantalla: int):
        """
        Inicializa el gestor de proyectiles.

        Args:
            ancho_pantalla: Ancho de la ventana del juego
            alto_pantalla: Alto de la ventana del juego
        """
        self._ancho = ancho_pantalla
        self._alto = alto_pantalla

        # Listas de proyectiles
        self.proyectiles: list[Proyectil] = []
        self.lista_sprites = arcade.SpriteList()

        # Timers de disparo de enemigos (cada enemigo tiene su propio timer)
        self._timers_disparo_enemigo: dict[Enemigo, float] = {}

        # Cooldown del jugador
        self._cooldown_jugador = 0.0

    @property
    def puede_disparar_jugador(self) -> bool:
        """Retorna True si el jugador puede disparar (cooldown expirado)."""
        return self._cooldown_jugador <= 0

    def establecer_cooldown_jugador(self, cooldown: float) -> None:
        """Establece el cooldown del jugador (usado por el sistema de mejoras)."""
        self._cooldown_jugador = cooldown

    def actualizar_cooldowns(self, delta_time: float) -> None:
        """Actualiza todos los cooldowns."""
        self._cooldown_jugador = max(0, self._cooldown_jugador - delta_time)

    def crear_proyectil_jugador(
        self,
        x: float,
        y: float,
        direccion_x: float,
        direccion_y: float,
        personaje,
    ) -> Proyectil | None:
        """
        Crea un proyectil disparado por el jugador.

        Args:
            x, y: Posición inicial
            direccion_x, direccion_y: Dirección normalizada del disparo
            personaje: Instancia del personaje para usar sus atributos de mejora

        Returns:
            El proyectil creado, o None si está en cooldown
        """
        if not self.puede_disparar_jugador:
            return None  # type: ignore

        # Normalizar dirección
        magnitud = (direccion_x**2 + direccion_y**2) ** 0.5
        if magnitud > 0:
            direccion_x /= magnitud
            direccion_y /= magnitud
        else:
            direccion_x, direccion_y = 0, -1  # Por defecto hacia abajo

        # Aplicar multiplicadores del personaje
        dano = int(self.DANO_PROYECTIL_JUGADOR * personaje.dano_proyectil)
        velocidad = self.VELOCIDAD_PROYECTIL_JUGADOR * personaje.velocidad_proyectil

        proyectil = Proyectil(
            x=x,
            y=y,
            direccion_x=direccion_x,
            direccion_y=direccion_y,
            dano=dano,
            velocidad=velocidad,
            es_del_jugador=True,
            rebotes=personaje.rebotes,
        )

        # Crear sprite
        sprite = self._crear_sprite_proyectil(proyectil)
        proyectil.sprite = sprite
        self.lista_sprites.append(sprite)
        self.proyectiles.append(proyectil)

        # Activar cooldown usando el atributo del personaje
        self._cooldown_jugador = personaje.cooldown_disparo

        return proyectil

    def crear_proyectil_enemigo(
        self,
        enemigo: Enemigo,
        target_x: float,
        target_y: float,
    ) -> Proyectil | None:
        """
        Crea un proyectil disparado por un enemigo hacia un objetivo.

        Args:
            enemigo: Enemigo que dispara
            target_x, target_y: Posición del objetivo (normalmente el jugador)

        Returns:
            El proyectil creado, o None si el enemigo no puede disparar
        """
        if not enemigo.tiene_sprite():
            return None

        # Inicializar timer si no existe (para el primer disparo)
        if enemigo not in self._timers_disparo_enemigo:
            self._timers_disparo_enemigo[enemigo] = random.uniform(
                self.COOLDOWN_MIN_ENEMIGO, self.COOLDOWN_MAX_ENEMIGO
            )
            return None

        # Verificar si el timer expiró (> 0 means cooldown ACTIVE, need <= 0 to fire)
        if self._timers_disparo_enemigo[enemigo] > 0:
            return None

        # Timer expiró -> crear proyectil
        # Calcular dirección hacia el objetivo
        dx = target_x - enemigo.sprite.center_x
        dy = target_y - enemigo.sprite.center_y

        magnitud = (dx**2 + dy**2) ** 0.5
        if magnitud > 0:
            dx /= magnitud
            dy /= magnitud

        proyectil = Proyectil(
            x=enemigo.sprite.center_x,
            y=enemigo.sprite.center_y,
            direccion_x=dx,
            direccion_y=dy,
            dano=self.DANO_PROYECTIL_ENEMIGO,
            velocidad=self.VELOCIDAD_PROYECTIL_ENEMIGO,
            es_del_jugador=False,
        )

        sprite = self._crear_sprite_proyectil(proyectil)
        proyectil.sprite = sprite
        self.lista_sprites.append(sprite)
        self.proyectiles.append(proyectil)

        # Reiniciar timer para el próximo disparo
        self._timers_disparo_enemigo[enemigo] = random.uniform(
            self.COOLDOWN_MIN_ENEMIGO, self.COOLDOWN_MAX_ENEMIGO
        )

        return proyectil

    def actualizar_timers_enemigos(self, delta_time: float) -> None:
        """Actualiza los timers de disparo de todos los enemigos."""
        for enemigo in self._timers_disparo_enemigo:
            self._timers_disparo_enemigo[enemigo] -= delta_time

    def actualizar_proyectiles(self, delta_time: float) -> list[Proyectil]:
        """
        Actualiza todos los proyectiles y retorna los que deben eliminarse.

        Args:
            delta_time: Tiempo transcurrido

        Returns:
            Lista de proyectiles que salieron de pantalla
        """
        fuera_de_pantalla = []

        for proyectil in self.proyectiles:
            if not proyectil.activo:
                continue

            # Actualizar posición
            proyectil.actualizar(delta_time)

            # Manejar rebotes si el proyectil tiene rebotes restantes
            if proyectil.rebotes_actuales > 0:
                proyectil.rebotar_en_pared(self._ancho, self._alto)

            # Sincronizar sprite
            if proyectil.sprite:
                proyectil.sprite.center_x = proyectil.center_x
                proyectil.sprite.center_y = proyectil.center_y

            # Verificar si salió de pantalla
            if proyectil.esta_fuera_de_pantalla(self._ancho, self._alto):
                fuera_de_pantalla.append(proyectil)

        return fuera_de_pantalla

    def verificar_colisiones_enemigos(
        self,
        enemigos: list[Enemigo],
        personaje: Personaje,
    ) -> tuple[list[tuple[Proyectil, Enemigo]], list[tuple[Proyectil, Personaje]]]:
        """
        Verifica colisiones de proyectiles.

        Returns:
            Tupla con (impactos_a_enemigos, impactos_al_jugador)
        """
        impactos_enemigos = []
        impactos_jugador = []

        for proyectil in self.proyectiles:
            if not proyectil.activo or not proyectil.sprite:
                continue

            if proyectil.es_del_jugador:
                # Proyectil del jugador -> verificar contra enemigos
                for enemigo in enemigos:
                    if enemigo.esta_vivo() and enemigo.sprite:
                        if arcade.check_for_collision(proyectil.sprite, enemigo.sprite):
                            # Marcar proyectil como inactivo INMEDIATAMENTE para evitar
                            # múltiples impactos en frames consecutivos
                            proyectil.activo = False
                            impactos_enemigos.append((proyectil, enemigo))
                            break
            else:
                # Proyectil del enemigo -> verificar contra jugador
                if personaje.sprite and arcade.check_for_collision(
                    proyectil.sprite, personaje.sprite
                ):
                    # Marcar proyectil como inactivo INMEDIATAMENTE para evitar
                    # múltiples impactos en frames consecutivos
                    proyectil.activo = False
                    impactos_jugador.append((proyectil, personaje))

        return impactos_enemigos, impactos_jugador

    def eliminar_proyectil(self, proyectil: Proyectil) -> None:
        """Elimina un proyectil del gestor."""
        proyectil.activo = False
        if proyectil.sprite and proyectil.sprite in self.lista_sprites:
            self.lista_sprites.remove(proyectil.sprite)
        if proyectil in self.proyectiles:
            self.proyectiles.remove(proyectil)

    def eliminar_enemigo(self, enemigo: Enemigo) -> None:
        """Limpia el timer de un enemigo eliminado."""
        if enemigo in self._timers_disparo_enemigo:
            del self._timers_disparo_enemigo[enemigo]

    def limpiar(self) -> None:
        """Limpia todos los proyectiles y timers."""
        self.proyectiles.clear()
        self.lista_sprites = arcade.SpriteList()
        self._timers_disparo_enemigo.clear()
        self._cooldown_jugador = 0.0

    def _crear_sprite_proyectil(self, proyectil: Proyectil) -> arcade.Sprite:
        """Crea el sprite visual de un proyectil."""
        color = arcade.color.CYAN if proyectil.es_del_jugador else arcade.color.ORANGE
        sprite = arcade.SpriteSolidColor(
            proyectil.tamaño, proyectil.tamaño, color=color
        )
        sprite.center_x = proyectil.center_x
        sprite.center_y = proyectil.center_y
        return sprite

    def dibujar(self) -> None:
        """Dibuja todos los proyectiles."""
        self.lista_sprites.draw()
