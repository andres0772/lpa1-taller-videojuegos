import arcade


class HUD:
    """Interfaz de usuario que muestra stats en pantalla."""

    def __init__(self, persona):
        self._personaje = persona

    def dibujar(self) -> None:
        """Dibuja el HUD en pantalla."""
        # Fondo del HUD
        arcade.draw_lrtb_rectangle_filled(
            left=10, right=250, top=90, bottom=10, color=(0, 0, 0, 180)
        )

        # Nombre del personaje
        arcade.draw_text(
            f"Héroe: {self._personaje.nombre}",
            20,
            70,
            arcade.color.WHITE,
            14,
            anchor_x="left",
            anchor_y="top",
        )

        # Nivel
        arcade.draw_text(
            f"Nivel: {self._personaje.nivel}",
            20,
            50,
            arcade.color.GOLD,
            14,
            anchor_x="left",
            anchor_y="top",
        )

        # HP
        hp_color = arcade.color.GREEN
        if self._personaje.hp_actual < self._personaje.hp_max * 0.3:
            hp_color = arcade.color.RED
        elif self._personaje.hp_actual < self._personaje.hp_max * 0.6:
            hp_color = arcade.color.YELLOW

        arcade.draw_text(
            f"HP: {self._personaje.hp_actual}/{self._personaje.hp_max}",
            20,
            30,
            hp_color,
            14,
            anchor_x="left",
            anchor_y="top",
        )

        # Oro
        arcade.draw_text(
            f"Oro: {self._personaje.oro}",
            130,
            50,
            arcade.color.GOLD,
            14,
            anchor_x="left",
            anchor_y="top",
        )

        # Experiencia
        arcade.draw_text(
            f"XP: {self._personaje.experiencia}/{self._personaje.experiencia_siguiente_nivel}",
            130,
            30,
            arcade.color.CYAN,
            14,
            anchor_x="left",
            anchor_y="top",
        )
