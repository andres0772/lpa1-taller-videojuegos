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
from src.ui import HUD, MenuTienda, MenuPausa
from src.items import Tesoro, TrampaExplosiva
from src.sistemas import SistemaCombate

ANCHO_VENTANA = 1080
ALTO_VENTANA = 720
TITULO = "Fantasy RPG - Taller POO"


class Juego(arcade.Window):
    """Clase principal del juego."""

    COMBATE_COOLDOWN = 1.0  # segundos entre ataques
    VELOCIDAD_JUGADOR = 150  # pixels por segundo
    VELOCIDAD_ENEMIGO = 50  # pixels por segundo (más lento que el jugador)

    def __init__(self):
        super().__init__(ANCHO_VENTANA, ALTO_VENTANA, TITULO)

        # Color de fondo según el área (inicial = bosque)
        self._actualizar_color_fondo()

        # Crear personaje
        self.personaje = Personaje("Heroe")

        # Cooldown de combate para evitar muerte por frame
        self._tiempo_ultimo_combate = 0.0

        # Keys presionadas para movimiento continuo
        self._keys_presionadas = set()

        # Crear escenario (las áreas ya generan su contenido automáticamente)
        self.escenario = Escenario(ANCHO_VENTANA, ALTO_VENTANA)

        # Crear HUD
        self.hud = HUD(self.personaje)

        # Crear menú de tienda
        self.tienda = MenuTienda(self.personaje, self.escenario)
        self._tienda_abierta = False

        # Crear menú de pausa
        self.pausa = MenuPausa(self.personaje)
        self._pausa_abierta = False

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

    def _actualizar_color_fondo(self):
        """Actualiza el color de fondo según el área actual."""
        color = self.escenario.color_fondo
        arcade.set_background_color(color)

    def _cargar_area_actual(self):
        """Carga los sprites del área actual."""
        # Limpiar sprites de enemigos e items previos (excepto jugador)
        for sprite in self.lista_sprites:
            if sprite != self.sprite_jugador:
                self.lista_sprites.remove(sprite)

        # Agregar enemigos del área actual
        for enemigo in self.escenario.enemigos:
            color = (
                arcade.color.GREEN if enemigo.tipo == "terrestre" else arcade.color.RED
            )
            sprite = self._crear_sprite_enemigo(enemigo, color)
            self.lista_sprites.append(sprite)
            enemigo.sprite = sprite

        # Agregar items del área actual
        for item in self.escenario.items:
            if isinstance(item, Tesoro):
                sprite = self._crear_sprite_item(arcade.color.GOLD)
                self.lista_sprites.append(sprite)
                item.sprite = sprite

    def _cambiar_area(self, tipo: str):
        """Cambia el área del juego."""
        if self.escenario.cambiar_area(tipo):
            self._actualizar_color_fondo()
            # Reiniciar posición del jugador en el centro
            self.sprite_jugador.center_x = ANCHO_VENTANA // 2
            self.sprite_jugador.center_y = ALTO_VENTANA // 2
            self._cargar_area_actual()
            print(f"¡Bienvenido a {self.escenario.nombre_area_actual}!")
            return True
        return False

    def on_key_press(self, key, modifiers):
        """Maneja eventos de teclado."""
        # Si la tienda está abierta, manejar input ahí
        if self._tienda_abierta:
            if key == arcade.key.ESCAPE:
                self._tienda_abierta = False
                self.tienda.cerrar()
            else:
                self.tienda.manejar_input(key)
            return

        # Si el menú de pausa está abierto, manejar input ahí
        if self._pausa_abierta:
            if key == arcade.key.ESCAPE:
                self._pausa_abierta = False
                self.pausa.cerrar()
            else:
                # Si el input cierra el menú (opción 1), cerrar pausa
                if self.pausa.manejar_input(key):
                    # Si la opción fue continuar o salir, cerrar pausa
                    if key in (arcade.key.NUM_1, arcade.key.KEY_1):
                        self._pausa_abierta = False
                    # Si salió del juego, ya se cerró solo
                    if key in (arcade.key.NUM_4, arcade.key.KEY_4):
                        pass  # El juego ya se cierra en MenuPausa
            return

        # Abrir menú de pausa con ESC o P
        if key in (arcade.key.ESCAPE, arcade.key.P):
            self._pausa_abierta = True
            self.pausa.abrir()
            return

        # Abrir tienda con 'T'
        if key == arcade.key.T:
            self._tienda_abierta = True
            self.tienda.abrir()
            return

        # Cambiar área con 'M'
        if key == arcade.key.M:
            self.escenario.ir_area_siguiente()
            self._actualizar_color_fondo()
            # Reiniciar posición del jugador en el centro
            self.sprite_jugador.center_x = ANCHO_VENTANA // 2
            self.sprite_jugador.center_y = ALTO_VENTANA // 2
            self._cargar_area_actual()
            print(f"¡Has entrado a {self.escenario.nombre_area_actual}!")
            return

        self._keys_presionadas.add(key)

    def on_key_release(self, key, modifiers):
        """Maneja cuando se suelta una tecla."""
        if key in self._keys_presionadas:
            self._keys_presionadas.remove(key)

    def on_update(self, delta_time):
        """Actualiza el estado del juego."""
        # No procesar si la tienda está abierta
        if self._tienda_abierta:
            return

        # No procesar si el menú de pausa está abierto
        if self._pausa_abierta:
            return

        # Movimiento continuo basado en keys presionadas
        velocidad = self.VELOCIDAD_JUGADOR * delta_time

        if arcade.key.LEFT in self._keys_presionadas:
            self.sprite_jugador.center_x -= velocidad
        if arcade.key.RIGHT in self._keys_presionadas:
            self.sprite_jugador.center_x += velocidad
        if arcade.key.UP in self._keys_presionadas:
            self.sprite_jugador.center_y += velocidad
        if arcade.key.DOWN in self._keys_presionadas:
            self.sprite_jugador.center_y -= velocidad

        # Mantener dentro de la pantalla
        self.sprite_jugador.center_x = max(
            20, min(ANCHO_VENTANA - 20, self.sprite_jugador.center_x)
        )
        self.sprite_jugador.center_y = max(
            20, min(ALTO_VENTANA - 20, self.sprite_jugador.center_y)
        )

        # Sincronizar posición del personaje
        self.personaje.center_x = self.sprite_jugador.center_x
        self.personaje.center_y = self.sprite_jugador.center_y

        # Actualizar movimiento de enemigos (persecución simple)
        for enemigo in self.escenario.enemigos:
            if enemigo.esta_vivo() and hasattr(enemigo, "sprite") and enemigo.sprite:
                # Calcular dirección hacia el jugador
                dx = self.sprite_jugador.center_x - enemigo.sprite.center_x
                dy = self.sprite_jugador.center_y - enemigo.sprite.center_y

                # Normalizar y mover lentamente hacia el jugador
                distancia = (dx**2 + dy**2) ** 0.5
                if distancia > 0:
                    velocidad_enemigo = self.VELOCIDAD_ENEMIGO * delta_time
                    # Los enemigos siempre se mueven hacia el jugador
                    # Se acercan hasta tener contacto físico
                    dx_normalizado = dx / distancia
                    dy_normalizado = dy / distancia
                    enemigo.sprite.center_x += dx_normalizado * velocidad_enemigo
                    enemigo.sprite.center_y += dy_normalizado * velocidad_enemigo

                # Mantener dentro de los límites de la pantalla
                enemigo.sprite.center_x = max(
                    20, min(ANCHO_VENTANA - 20, enemigo.sprite.center_x)
                )
                enemigo.sprite.center_y = max(
                    20, min(ALTO_VENTANA - 20, enemigo.sprite.center_y)
                )

                # Sincronizar posición con el objeto Enemigo
                enemigo.center_x = enemigo.sprite.center_x
                enemigo.center_y = enemigo.sprite.center_y

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
                    elif isinstance(item, TrampaExplosiva):
                        dano = item.daño
                        item.activar(self.personaje)
                        print(f"¡TRAMPA! Daño recibido: {dano}")
                        if item.sprite in self.lista_sprites:
                            self.lista_sprites.remove(item.sprite)
                        self.escenario.items.remove(item)

        # Verificar si el personaje murió
        if not self.personaje.esta_vivo():
            print("💀 GAME OVER 💀")
            print("El personaje ha muerto. Cerrando el juego...")
            arcade.close_window()
            return

    def on_draw(self):
        """Dibuja el juego."""
        # Limpiar la pantalla cada frame para evitar rastros
        self.clear()

        # El background color ya se configuró en __init__

        # Dibujar sprites
        self.lista_sprites.draw()

        # Dibujar HUD
        self.hud.dibujar()

        # Dibujar tienda si está abierta
        if self._tienda_abierta:
            self.tienda.dibujar()

        # Dibujar menú de pausa si está abierto
        if self._pausa_abierta:
            self.pausa.dibujar()

        # Instrucciones
        arcade.draw_text(
            "Flechas: mover | [T] Tienda | [M] Cambiar área | [ESC/P] Pausa",
            ANCHO_VENTANA // 2,
            ALTO_VENTANA - 30,
            arcade.color.WHITE,
            16,
            anchor_x="center",
        )

        # Mostrar nombre del área actual
        arcade.draw_text(
            f"Área: {self.escenario.nombre_area_actual}",
            100,
            ALTO_VENTANA - 30,
            arcade.color.WHITE,
            14,
            anchor_x="left",
        )


def main():
    """Función principal."""
    ventana = Juego()
    arcade.run()


if __name__ == "__main__":
    main()
