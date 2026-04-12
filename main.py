"""Fantasy RPG - Taller de POO

Juego de demostración para aprender Programación Orientada a Objetos.
"""

import sys
import os

# Agregar este directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcade
from src.entidades import Personaje, Enemigo
from src.mundo import Escenario
from src.ui import HUD
from src.items import Tesoro, TrampaExplosiva
from src.sistemas import SistemaCombate

ANCHO_VENTANA = 1080
ALTO_VENTANA = 720
TITULO = "Fantasy RPG - Taller POO"


class Juego(arcade.Window):
    """Clase principal del juego."""

    COMBATE_COOLDOWN = 1.0  # segundos entre ataques

    def __init__(self):
        super().__init__(ANCHO_VENTANA, ALTO_VENTANA, TITULO)

        # Color de fondo (verde oscuro = bosque)
        arcade.set_background_color(arcade.color.DARK_GREEN)

        # Crear personaje
        self.personaje = Personaje("Heroe")

        # Cooldown de combate para evitar muerte por frame
        self._tiempo_ultimo_combate = 0.0

        # Crear escenario
        self.escenario = Escenario(ANCHO_VENTANA, ALTO_VENTANA)
        self.escenario.generar_enemigos_aleatorios(3)
        self.escenario.generar_items_aleatorios(2)

        # Crear HUD
        self.hud = HUD(self.personaje)

        # Sprite del personaje (rectángulo azul)
        self.sprite_jugador = None
        self._crear_sprite_jugador()

        # Lista de sprites para renderizado
        self.lista_sprites = arcade.SpriteList()
        self.lista_sprites.append(self.sprite_jugador)

        # Agregar enemigos como sprites
        for enemigo in self.escenario.enemigos:
            color = (
                arcade.color.GREEN if enemigo.tipo == "terrestre" else arcade.color.RED
            )
            sprite = self._crear_sprite_enemigo(enemigo, color)
            self.lista_sprites.append(sprite)
            enemigo.sprite = sprite

        # Agregar items como sprites
        for item in self.escenario.items:
            if isinstance(item, Tesoro):
                sprite = self._crear_sprite_item(arcade.color.GOLD)
                self.lista_sprites.append(sprite)
                item.sprite = sprite

    def _crear_sprite_jugador(self):
        """Crea el sprite del jugador (rectángulo azul)."""
        sprite = arcade.SpriteSolidColor(40, 40, color=arcade.color.BLUE)
        sprite.center_x = ANCHO_VENTANA // 2
        sprite.center_y = ALTO_VENTANA // 2
        self.sprite_jugador = sprite

    def _crear_sprite_enemigo(self, enemigo: Enemigo, color):
        """Crea el sprite de un enemigo."""
        size = 35
        sprite = arcade.SpriteSolidColor(size, size, color=color)
        sprite.center_x = enemigo.center_x
        sprite.center_y = enemigo.center_y
        return sprite

    def _crear_sprite_item(self, color):
        """Crea el sprite de un item."""
        sprite = arcade.SpriteSolidColor(20, 20, color=color)
        return sprite

    def on_key_press(self, key, modifiers):
        """Maneja eventos de teclado."""
        velocidad = 10

        if key == arcade.key.LEFT:
            self.sprite_jugador.center_x -= velocidad
        elif key == arcade.key.RIGHT:
            self.sprite_jugador.center_x += velocidad
        elif key == arcade.key.UP:
            self.sprite_jugador.center_y += velocidad
        elif key == arcade.key.DOWN:
            self.sprite_jugador.center_y -= velocidad

        # Mantener dentro de la pantalla
        self.sprite_jugador.center_x = max(
            20, min(ANCHO_VENTANA - 20, self.sprite_jugador.center_x)
        )
        self.sprite_jugador.center_y = max(
            20, min(ALTO_VENTANA - 20, self.sprite_jugador.center_y)
        )

    def on_update(self, delta_time):
        """Actualiza el estado del juego."""
        # Sincronizar posición del personaje
        self.personaje.center_x = self.sprite_jugador.center_x
        self.personaje.center_y = self.sprite_jugador.center_y

        # Actualizar cooldown de combate
        self._tiempo_ultimo_combate -= delta_time

        # Verificar colisiones con enemigos (solo si no está en cooldown)
        if self._tiempo_ultimo_combate <= 0:
            for enemigo in list(
                self.escenario.enemigos
            ):  # Usar list() para poder modificar
                if (
                    enemigo.esta_vivo()
                    and hasattr(enemigo, "sprite")
                    and enemigo.sprite
                ):
                    if arcade.check_for_collision(self.sprite_jugador, enemigo.sprite):
                        # ¡Combate!
                        resultado = SistemaCombate.atacar(self.personaje, enemigo)
                        print(f"¡Combate! Daño: {resultado.dano_infligido}")

                        if resultado.enemigo_derrotado:
                            # Ganar experiencia y oro
                            self.personaje.ganar_experiencia(
                                enemigo.experiencia_al_derrotar
                            )
                            self.personaje._oro += enemigo.oro_al_derrotar
                            print(
                                f"¡Enemigo derrotado! +{enemigo.experiencia_al_derrotar} XP, +{enemigo.oro_al_derrotar} oro"
                            )
                            # Eliminar sprite
                            if enemigo.sprite in self.lista_sprites:
                                self.lista_sprites.remove(enemigo.sprite)
                            # Remover enemigo de la lista
                            self.escenario.enemigos.remove(enemigo)

                        # Activar cooldown
                        self._tiempo_ultimo_combate = self.COMBATE_COOLDOWN
                        break  # Solo un combate por frame

        # Verificar colisiones con items
        for item in list(self.escenario.items):
            if hasattr(item, "sprite") and item.sprite:
                if arcade.check_for_collision(self.sprite_jugador, item.sprite):
                    if isinstance(item, Tesoro):
                        self.personaje._oro += item.valor
                        print(f"¡Tesoro encontrado! +{item.valor} oro")
                        if item.sprite in self.lista_sprites:
                            self.lista_sprites.remove(item.sprite)
                        self.escenario.items.remove(item)

    def on_draw(self):
        """Dibuja el juego."""
        # El background color ya se configuró en __init__

        # Dibujar sprites
        self.lista_sprites.draw()

        # Dibujar HUD
        self.hud.dibujar()

        # Instrucciones
        arcade.draw_text(
            "Usa flechas para moverte",
            ANCHO_VENTANA // 2,
            ALTO_VENTANA - 30,
            arcade.color.WHITE,
            16,
            anchor_x="center",
        )


def main():
    """Función principal."""
    ventana = Juego()
    arcade.run()


if __name__ == "__main__":
    main()
