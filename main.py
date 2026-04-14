"""Fantasy RPG - Taller de POO

Juego de demostración para aprender Programación Orientada a Objetos.
"""

import sys
import os

# Agregar este directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcade
import random
from src.entidades import Personaje, Enemigo, Proyectil
from src.mundo import Escenario
from src.ui import HUD, MenuTienda, MenuPausa
from src.items import Tesoro, TrampaExplosiva
from src.sistemas import SistemaCombate, GestorProyectiles, GestorCombate, GestorItems

ANCHO_VENTANA = 1080
ALTO_VENTANA = 720
TITULO = "Fantasy RPG - Taller POO"


class Juego(arcade.Window):
    """Clase principal del juego."""

    COMBATE_COOLDOWN = 1.0  # segundos entre ataques
    ATAQUE_COOLDOWN = 0.5  # segundos entre ataques del jugador
    RADIO_ATAQUE = 60  # pixels de alcance para atacar
    VELOCIDAD_JUGADOR = 150  # pixels por segundo
    VELOCIDAD_ENEMIGO = 50  # pixels por segundo (más lento que el jugador)
    PUNTAJE_VICTORIA = 1000  # puntos necesarios para victoria por puntaje

    def __init__(self):
        super().__init__(ANCHO_VENTANA, ALTO_VENTANA, TITULO)

        # Crear personaje
        self.personaje = Personaje("Heroe")

        # Cooldown de ataque del jugador
        self._tiempo_ultimo_ataque = 0.0

        # Feedback visual de ataque
        self._jugador_atacando = False
        self._tiempo_ataque_fx = 0.0

        # Dirección actual del jugador (para disparar)
        self._direccion_disparo = (0, -1)  # Por defecto dispara hacia abajo

        # Áreas visitadas (para victoria por exploración)
        self._areas_visitadas: set[str] = set()
        self._areas_visitadas.add("bosque")  # Área inicial cuenta como visitada
        self._juego_terminado = False
        self._mensaje_victoria = ""

        # Keys presionadas para movimiento continuo
        self._keys_presionadas = set()

        # Crear escenario (las áreas ya generan su contenido automáticamente)
        self.escenario = Escenario(ANCHO_VENTANA, ALTO_VENTANA)

        # Color de fondo según el área (inicial = bosque)
        self._actualizar_color_fondo()

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

        # Gestor de proyectiles (refactoring: extraído de Juego)
        self.gestor_proyectiles = GestorProyectiles(ANCHO_VENTANA, ALTO_VENTANA)
        self.gestor_combate = GestorCombate()
        self.gestor_items = GestorItems()

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

        # Nivel del juego (progresivo)
        self._nivel_juego = 1

        # Agregar sprite del personaje al gestor de proyectiles
        self.personaje.sprite = self.sprite_jugador

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
        # Limpiar TODOS los sprites excepto el jugador
        self.lista_sprites.clear()
        self.lista_sprites.append(self.sprite_jugador)

        # Regenerar contenido del área (nuevos enemigos y items)
        self.escenario.regenerar_contenido()

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

            # Registrar área como visitada
            self._areas_visitadas.add(self.escenario.area_actual)

            # Limpiar sprites anteriores (excepto el jugador)
            self.lista_sprites.clear()
            self.lista_sprites.append(self.sprite_jugador)

            # Limpiar proyectiles usando el gestor
            self.gestor_proyectiles.limpiar()

            # Reiniciar posición del jugador en el centro
            self.sprite_jugador.center_x = ANCHO_VENTANA // 2
            self.sprite_jugador.center_y = ALTO_VENTANA // 2
            self._cargar_area_actual()
            print(f"¡Bienvenido a {self.escenario.nombre_area_actual}!")
            return True
        return False

    def on_key_press(self, key, modifiers):
        """Maneja eventos de teclado."""
        # Si el juego terminó y se presiona ESC, cerrar
        if self._juego_terminado:
            if key == arcade.key.ESCAPE:
                arcade.close_window()
            return

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
            # Registrar área como visitada
            self._areas_visitadas.add(self.escenario.area_actual)
            # Reiniciar posición del jugador en el centro
            self.sprite_jugador.center_x = ANCHO_VENTANA // 2
            self.sprite_jugador.center_y = ALTO_VENTANA // 2
            self._cargar_area_actual()
            print(f"¡Has entrado a {self.escenario.nombre_area_actual}!")
            return

        # Atacar con ESPACIO
        if key == arcade.key.SPACE:
            self._intentar_disparar()
            return

        # Rastrear dirección para el disparo
        if key == arcade.key.LEFT:
            self._direccion_disparo = (-1, 0)
        elif key == arcade.key.RIGHT:
            self._direccion_disparo = (1, 0)
        elif key == arcade.key.UP:
            self._direccion_disparo = (0, 1)
        elif key == arcade.key.DOWN:
            self._direccion_disparo = (0, -1)

        self._keys_presionadas.add(key)

    def on_key_release(self, key, modifiers):
        """Maneja cuando se suelta una tecla."""
        if key in self._keys_presionadas:
            self._keys_presionadas.remove(key)

    def _intentar_disparar(self):
        """Intenta disparar un proyectil usando el gestor."""
        if self._juego_terminado:
            return

        # Obtener dirección normalizada
        dx, dy = self._direccion_disparo

        # Si no hay dirección, usar hacia abajo
        if dx == 0 and dy == 0:
            dx, dy = 0, -1

        # Crear proyectil usando el gestor
        proyectil = self.gestor_proyectiles.crear_proyectil_jugador(
            x=self.sprite_jugador.center_x,
            y=self.sprite_jugador.center_y,
            direccion_x=dx,
            direccion_y=dy,
        )

        if proyectil:
            print(f"¡DISPARO! Daño: {proyectil.dano}")

    def _verificar_victoria(self):
        """Verifica si se cumple alguna condición de victoria."""
        if self._juego_terminado:
            return

        # R7.1: Victoria por Exploración
        if len(self._areas_visitadas) >= 3:
            self._juego_terminado = True
            self._mensaje_victoria = "¡Has explorado todo! ¡VICTORIA!"
            return

        # R7.3: Victoria por Puntaje (experiencia + oro)
        puntaje = self.personaje.experiencia + self.personaje.oro
        if puntaje >= self.PUNTAJE_VICTORIA:
            self._juego_terminado = True
            self._mensaje_victoria = "¡Has alcanzado el puntaje máximo! ¡VICTORIA!"
            return

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

        # Actualizar timers de DISPARO de enemigos ANTES de que intenten disparar
        self.gestor_proyectiles.actualizar_timers_enemigos(delta_time)

        # Actualizar movimiento de enemigos (persecución simple)
        for enemigo in self.escenario.enemigos:
            if enemigo.esta_vivo() and enemigo.tiene_sprite():
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

                # Enemigo intenta disparar al jugador
                proyectil = self.gestor_proyectiles.crear_proyectil_enemigo(
                    enemigo=enemigo,
                    target_x=self.sprite_jugador.center_x,
                    target_y=self.sprite_jugador.center_y,
                )
                if proyectil:
                    print(f"¡PROYECTIL ENEMIGO! Daño: {proyectil.dano}")

        # Actualizar cooldowns
        self.gestor_combate.actualizar_cooldown(delta_time)
        self._tiempo_ultimo_ataque -= delta_time

        # Actualizar cooldowns del gestor de proyectiles
        self.gestor_proyectiles.actualizar_cooldowns(delta_time)

        # Actualizar proyectiles usando el gestor
        fuera_de_pantalla = self.gestor_proyectiles.actualizar_proyectiles(delta_time)
        for proyectil in fuera_de_pantalla:
            self.gestor_proyectiles.eliminar_proyectil(proyectil)

        # Verificar colisiones de proyectiles
        impactos_enemigos, impactos_jugador = (
            self.gestor_proyectiles.verificar_colisiones_enemigos(
                self.escenario.enemigos, self.personaje
            )
        )

        # Procesar impactos a enemigos
        for proyectil, enemigo in impactos_enemigos:
            enemigo.recibir_daño(proyectil.dano)
            print(f"¡IMPACTO! Proyectil causó {proyectil.dano} daño")

            if not enemigo.esta_vivo():
                self.personaje.ganar_experiencia(enemigo.experiencia_al_derrotar)
                self.personaje.agregar_oro(enemigo.oro_al_derrotar)
                print(
                    f"¡Enemigo derrotado! +{enemigo.experiencia_al_derrotar} XP, +{enemigo.oro_al_derrotar} oro"
                )

                if enemigo.es_jefe:
                    self._juego_terminado = True
                    self._mensaje_victoria = "¡Has derrotado al JEFE! ¡VICTORIA!"

                if enemigo.sprite in self.lista_sprites:
                    self.lista_sprites.remove(enemigo.sprite)
                self.gestor_proyectiles.eliminar_enemigo(enemigo)
                self.escenario.enemigos.remove(enemigo)

            self.gestor_proyectiles.eliminar_proyectil(proyectil)

        # Procesar impactos al jugador
        for proyectil, personaje in impactos_jugador:
            personaje.recibir_daño(proyectil.dano)
            print(f"¡PROYECTIL ENEMIGO! Daño recibido: {proyectil.dano}")
            self.gestor_proyectiles.eliminar_proyectil(proyectil)

        # Actualizar efecto visual de ataque
        if self._tiempo_ataque_fx > 0:
            self._tiempo_ataque_fx -= delta_time
            if self._tiempo_ataque_fx <= 0:
                self._jugador_atacando = False

        # Verificar colisiones con enemigos (solo si no está en cooldown)
        resultado = self.gestor_combate.verificar_combate(
            self.personaje,
            self.sprite_jugador,
            self.escenario.enemigos,
            self.lista_sprites,
            on_enemigo_derrotado=lambda e: print(
                f"¡Enemigo derrotado! +{e.experiencia_al_derrotar} XP"
            ),
            on_jefe_derrotado=lambda: (
                setattr(self, "_juego_terminado", True)
                or setattr(
                    self, "_mensaje_victoria", "¡Has derrotado al JEFE! ¡VICTORIA!"
                )
            ),
        )
        if resultado:
            print(f"¡Combate! Daño: {resultado.dano_infligido} ")

        # Verificar colisiones con items
        self.gestor_items.verificar_colisiones(
            self.personaje,
            self.sprite_jugador,
            self.escenario.items,
            self.lista_sprites,
            on_tesoro_recogido=lambda oro: print(f"¡Tesoro encontrado! +{oro} oro"),
            on_trampa_activada=lambda dano: print(f"¡TRAMPA! Daño recibido: {dano}"),
        )

        # Verificar si TODOS los enemigos fueron derrotados → cambio automático de nivel
        if not self.escenario.enemigos and not self._juego_terminado:
            # Aumentar nivel del juego
            self._nivel_juego += 1
            # Subir nivel del escenario (dificultad progresiva)
            self.escenario.subir_nivel()
            # Avanzar al área siguiente
            self.escenario.ir_area_siguiente()
            self._actualizar_color_fondo()
            # Registrar área como visitada
            self._areas_visitadas.add(self.escenario.area_actual)
            # Reiniciar posición del jugador en el centro
            self.sprite_jugador.center_x = ANCHO_VENTANA // 2
            self.sprite_jugador.center_y = ALTO_VENTANA // 2
            # Cargar nuevo contenido
            self._cargar_area_actual()
            print(
                f"¡Todos los enemigos derrotados! Nivel {self._nivel_juego} - ¡Has entrado a {self.escenario.nombre_area_actual}!"
            )

        # Verificar condiciones de victoria
        self._verificar_victoria()

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

        # Dibujar proyectiles
        self.gestor_proyectiles.dibujar()

        # Dibujar HUD
        self.hud.dibujar()

        # Dibujar tienda si está abierta
        if self._tienda_abierta:
            self.tienda.dibujar()

        # Dibujar menú de pausa si está abierto
        if self._pausa_abierta:
            self.pausa.dibujar()

        # Feedback visual de ataque (cambiar color del jugador temporalmente)
        if self._jugador_atacando:
            self.sprite_jugador.color = arcade.color.YELLOW
        else:
            self.sprite_jugador.color = arcade.color.BLUE

        # Instrucciones
        arcade.draw_text(
            "Flechas: mover | [ESPACIO] Disparar | [T] Tienda | [M] Cambiar área | [ESC/P] Pausa",
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

        # Mostrar mensaje de victoria si el juego terminó
        if self._juego_terminado and self._mensaje_victoria:
            arcade.draw_text(
                self._mensaje_victoria,
                ANCHO_VENTANA // 2,
                ALTO_VENTANA // 2,
                arcade.color.GOLD,
                32,
                anchor_x="center",
                bold=True,
            )
            arcade.draw_text(
                "Presiona [ESC] para salir",
                ANCHO_VENTANA // 2,
                ALTO_VENTANA // 2 - 50,
                arcade.color.WHITE,
                18,
                anchor_x="center",
            )


def main():
    """Función principal."""
    ventana = Juego()
    arcade.run()


if __name__ == "__main__":
    main()
