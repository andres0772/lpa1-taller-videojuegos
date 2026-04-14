import pytest
from src.entidades.proyectil import Proyectil
from src.entidades.entidad import Entidad


class TestProyectil:
    """Tests para la clase Proyectil."""

    def test_herencia(self):
        """Verifica que Proyectil hereda de Entidad."""
        proyectil = Proyectil(0, 0, 0, 0, 10)
        assert isinstance(proyectil, Entidad), "Proyectil debe heredar de Entidad"

    def test_puede_recibir_daño(self):
        """Verifica que los proyectiles pueden recibir daño cuando están activos."""
        proyectil = Proyectil(0, 0, 0, 0, 10)
        assert proyectil.puede_recibir_daño(), (
            "Los proyectiles activos deben poder recibir daño"
        )

        proyectil.activo = False
        assert not proyectil.puede_recibir_daño(), (
            "Los proyectiles inactivos no deben poder recibir daño"
        )

    def test_puede_ser_destruido(self):
        """Verifica que los proyectiles se destruyen cuando están inactivos o con HP <= 0."""
        proyectil = Proyectil(0, 0, 0, 0, 10)
        proyectil.activo = False
        assert proyectil.puede_ser_destruido(), (
            "Los proyectiles inactivos deben poder ser destruidos"
        )

        proyectil.activo = True
        proyectil.recibir_daño(1)
        assert proyectil.puede_ser_destruido(), (
            "Los proyectiles con HP <= 0 deben poder ser destruidos"
        )

    def test_esta_vivo(self):
        """Verifica que el estado 'vivo' de los proyectiles funciona correctamente."""
        proyectil = Proyectil(0, 0, 0, 0, 10)
        assert proyectil.esta_vivo(), (
            "Los proyectiles activos con HP > 0 deben estar vivos"
        )

        proyectil.recibir_daño(1)
        assert not proyectil.esta_vivo(), (
            "Los proyectiles con HP <= 0 no deben estar vivos"
        )

        proyectil.activo = False
        assert not proyectil.esta_vivo(), (
            "Los proyectiles inactivos no deben estar vivos"
        )

    def test_color(self):
        """Verifica que los proyectiles tienen el color correcto según quién los dispara."""
        proyectil_jugador = Proyectil(0, 0, 0, 0, 10, es_del_jugador=True)
        assert proyectil_jugador.color == (0, 255, 255), (
            "Los proyectiles del jugador deben ser cyan"
        )

        proyectil_enemigo = Proyectil(0, 0, 0, 0, 10, es_del_jugador=False)
        assert proyectil_enemigo.color == (255, 165, 0), (
            "Los proyectiles de enemigos deben ser naranja"
        )

    def test_tamaño(self):
        """Verifica que los proyectiles tienen el tamaño correcto."""
        proyectil = Proyectil(0, 0, 0, 0, 10)
        assert proyectil.tamaño == 10, "El tamaño del proyectil debe ser 10"

    def test_actualizar(self):
        """Verifica que los proyectiles se mueven correctamente."""
        proyectil = Proyectil(0, 0, 1, 0, 10, velocidad=100)
        proyectil.actualizar(1.0)  # 1 segundo
        assert proyectil.center_x == 100, (
            "El proyectil debe moverse 100 unidades en 1 segundo"
        )

        proyectil.activo = False
        proyectil.center_x = 0
        proyectil.actualizar(1.0)
        assert proyectil.center_x == 0, "Los proyectiles inactivos no deben moverse"

    def test_esta_fuera_de_pantalla(self):
        """Verifica que los proyectiles detectan correctamente cuando salen de pantalla."""
        proyectil = Proyectil(0, 0, 0, 0, 10)
        assert not proyectil.esta_fuera_de_pantalla(100, 100), (
            "El proyectil debe estar dentro de la pantalla"
        )

        proyectil.center_x = -1
        assert proyectil.esta_fuera_de_pantalla(100, 100), (
            "El proyectil debe estar fuera de la pantalla por izquierda"
        )

        proyectil.center_x = 101
        assert proyectil.esta_fuera_de_pantalla(100, 100), (
            "El proyectil debe estar fuera de la pantalla por derecha"
        )

        proyectil.center_x = 50
        proyectil.center_y = -1
        assert proyectil.esta_fuera_de_pantalla(100, 100), (
            "El proyectil debe estar fuera de la pantalla por abajo"
        )

        proyectil.center_y = 101
        assert proyectil.esta_fuera_de_pantalla(100, 100), (
            "El proyectil debe estar fuera de la pantalla por arriba"
        )

    def test_dano(self):
        """Verifica que los proyectiles tienen el daño correcto."""
        proyectil = Proyectil(0, 0, 0, 0, 15)
        assert proyectil.dano == 15, "El daño del proyectil debe ser 15"

    def test_posicion(self):
        """Verifica que los proyectiles tienen la posición correcta."""
        proyectil = Proyectil(10, 20, 0, 0, 10)
        assert proyectil.posicion == (10, 20), (
            "La posición del proyectil debe ser (10, 20)"
        )

    def test_direccion(self):
        """Verifica que los proyectiles tienen la dirección correcta."""
        proyectil = Proyectil(0, 0, 0.5, 0.5, 10)
        assert proyectil.direccion == (0.5, 0.5), (
            "La dirección del proyectil debe ser (0.5, 0.5)"
        )

    def test_repr(self):
        """Verifica que la representación del proyectil es correcta."""
        proyectil = Proyectil(10, 20, 0, 0, 15, es_del_jugador=True)
        assert "Proyectil(jugador, dano=15, pos=10,20)" in str(proyectil), (
            "La representación del proyectil debe incluir tipo, daño y posición"
        )

        proyectil = Proyectil(10, 20, 0, 0, 15, es_del_jugador=False)
        assert "Proyectil(enemigo, dano=15, pos=10,20)" in str(proyectil), (
            "La representación del proyectil debe incluir tipo, daño y posición"
        )
