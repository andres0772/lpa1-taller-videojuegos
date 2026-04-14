import pytest
from src.sistemas.gestor_proyectiles import GestorProyectiles
from src.entidades.proyectil import Proyectil
from src.entidades.enemigo import Enemigo


class TestGestorProyectiles:
    """Tests para la clase GestorProyectiles."""

    def test_inicializacion(self):
        """Verifica que el gestor se inicializa correctamente."""
        gestor = GestorProyectiles(800, 600)
        assert gestor._ancho == 800, "El ancho debe ser 800"
        assert gestor._alto == 600, "El alto debe ser 600"
        assert len(gestor.proyectiles) == 0, (
            "Debe inicializar con lista vacía de proyectiles"
        )
        assert len(gestor.lista_sprites) == 0, (
            "Debe inicializar con lista vacía de sprites"
        )
        assert len(gestor._timers_disparo_enemigo) == 0, (
            "Debe inicializar con diccionario vacío de timers"
        )
        assert gestor._cooldown_jugador == 0.0, "El cooldown del jugador debe ser 0"

    def test_puede_disparar_jugador(self):
        """Verifica que el jugador puede disparar cuando el cooldown está en 0."""
        gestor = GestorProyectiles(800, 600)
        assert gestor.puede_disparar_jugador, (
            "El jugador debe poder disparar cuando el cooldown está en 0"
        )

        gestor._cooldown_jugador = 1.0
        assert not gestor.puede_disparar_jugador, (
            "El jugador no debe poder disparar cuando el cooldown está activo"
        )

    def test_actualizar_cooldowns(self):
        """Verifica que los cooldowns se actualizan correctamente."""
        gestor = GestorProyectiles(800, 600)
        gestor._cooldown_jugador = 1.0
        gestor.actualizar_cooldowns(0.5)
        assert gestor._cooldown_jugador == 0.5, (
            "El cooldown del jugador debe reducirse en 0.5 segundos"
        )

        gestor.actualizar_cooldowns(1.0)
        assert gestor._cooldown_jugador == 0.0, (
            "El cooldown del jugador no debe ser negativo"
        )

    def test_crear_proyectil_jugador(self):
        """Verifica que se crean proyectiles del jugador correctamente."""
        gestor = GestorProyectiles(800, 600)
        proyectil = gestor.crear_proyectil_jugador(100, 100, 0, 1)
        assert proyectil is not None, "Debe crear un proyectil"
        assert proyectil.es_del_jugador, "El proyectil debe ser del jugador"
        assert proyectil.center_x == 100, "La posición X debe ser 100"
        assert proyectil.center_y == 100, "La posición Y debe ser 100"
        assert proyectil.direccion_y == 1, "La dirección Y debe ser 1"
        assert gestor._cooldown_jugador > 0, "Debe activar el cooldown del jugador"

        # Verificar que no se puede crear otro proyectil mientras está en cooldown
        proyectil = gestor.crear_proyectil_jugador(100, 100, 0, 1)
        assert proyectil is None, "No debe crear un proyectil mientras está en cooldown"

    def test_crear_proyectil_enemigo(self):
        """Verifica que se crean proyectiles de enemigos correctamente."""
        gestor = GestorProyectiles(800, 600)
        enemigo = Enemigo(
            "TestEnemy", hp_max=50, ataque=10, defensa=5, tipo="terrestre"
        )
        enemigo.sprite = type("Sprite", (), {"center_x": 100, "center_y": 100})

        # Inicializar timer
        gestor._timers_disparo_enemigo[enemigo] = 0.0
        proyectil = gestor.crear_proyectil_enemigo(enemigo, 200, 200)
        assert proyectil is not None, "Debe crear un proyectil"
        assert not proyectil.es_del_jugador, "El proyectil debe ser del enemigo"
        assert proyectil.center_x == 100, "La posición X debe ser 100"
        assert proyectil.center_y == 100, "La posición Y debe ser 100"

        # Verificar dirección hacia el objetivo
        dx = proyectil.direccion_x
        dy = proyectil.direccion_y
        assert dx > 0, "La dirección X debe ser positiva"
        assert dy > 0, "La dirección Y debe ser positiva"

        # Verificar que no se puede crear otro proyectil mientras está en cooldown
        proyectil = gestor.crear_proyectil_enemigo(enemigo, 200, 200)
        assert proyectil is None, "No debe crear un proyectil mientras está en cooldown"

    def test_actualizar_timers_enemigos(self):
        """Verifica que los timers de enemigos se actualizan correctamente."""
        gestor = GestorProyectiles(800, 600)
        enemigo = Enemigo(
            "TestEnemy", hp_max=50, ataque=10, defensa=5, tipo="terrestre"
        )
        gestor._timers_disparo_enemigo[enemigo] = 1.0

        gestor.actualizar_timers_enemigos(0.5)
        assert gestor._timers_disparo_enemigo[enemigo] == 0.5, (
            "El timer debe reducirse en 0.5 segundos"
        )

        gestor.actualizar_timers_enemigos(1.0)
        assert gestor._timers_disparo_enemigo[enemigo] == -0.5, (
            "El timer puede ser negativo"
        )

    def test_actualizar_proyectiles(self):
        """Verifica que los proyectiles se actualizan correctamente."""
        gestor = GestorProyectiles(800, 600)
        proyectil = Proyectil(100, 100, 0, 1, 10, velocidad=100)
        proyectil.sprite = type("Sprite", (), {"center_x": 100, "center_y": 100})
        gestor.proyectiles.append(proyectil)
        # Skip lista_sprites to avoid arcade dependency in tests

        fuera_de_pantalla = gestor.actualizar_proyectiles(1.0)
        assert len(fuera_de_pantalla) == 0, (
            "No debe haber proyectiles fuera de pantalla"
        )
        assert proyectil.center_y == 200, (
            "El proyectil debe moverse 100 unidades en 1 segundo"
        )

        # Mover proyectil fuera de pantalla
        proyectil.center_y = 700
        fuera_de_pantalla = gestor.actualizar_proyectiles(0.0)
        assert len(fuera_de_pantalla) == 1, (
            "Debe detectar proyectiles fuera de pantalla"
        )

    @pytest.mark.skip(reason="Requires real arcade.Sprite instances - integration test")
    def test_verificar_colisiones_enemigos(self):
        """Verifica que se detectan colisiones correctamente."""
        gestor = GestorProyectiles(800, 600)
        enemigo = Enemigo(
            "TestEnemy", hp_max=50, ataque=10, defensa=5, tipo="terrestre"
        )
        enemigo.sprite = type("Sprite", (), {"center_x": 100, "center_y": 100})
        personaje = type(
            "Personaje",
            (),
            {"sprite": type("Sprite", (), {"center_x": 200, "center_y": 200})},
        )

        # Proyectil del jugador colisionando con enemigo
        proyectil_jugador = Proyectil(100, 100, 0, 1, 10, es_del_jugador=True)
        proyectil_jugador.sprite = type(
            "Sprite", (), {"center_x": 100, "center_y": 100}
        )
        gestor.proyectiles.append(proyectil_jugador)

        # Proyectil del enemigo colisionando con jugador
        proyectil_enemigo = Proyectil(200, 200, 0, 1, 10, es_del_jugador=False)
        proyectil_enemigo.sprite = type(
            "Sprite", (), {"center_x": 200, "center_y": 200}
        )
        gestor.proyectiles.append(proyectil_enemigo)

        impactos_enemigos, impactos_jugador = gestor.verificar_colisiones_enemigos(
            [enemigo], personaje
        )
        assert len(impactos_enemigos) == 1, "Debe detectar impacto a enemigo"
        assert len(impactos_jugador) == 1, "Debe detectar impacto al jugador"

    def test_eliminar_proyectil(self):
        """Verifica que se eliminan proyectiles correctamente."""
        gestor = GestorProyectiles(800, 600)
        proyectil = Proyectil(100, 100, 0, 1, 10)
        proyectil.sprite = type("Sprite", (), {"center_x": 100, "center_y": 100})
        gestor.proyectiles.append(proyectil)
        # Skip lista_sprites to avoid arcade dependency in tests

        gestor.eliminar_proyectil(proyectil)
        assert not proyectil.activo, "El proyectil debe estar inactivo"
        assert proyectil not in gestor.proyectiles, (
            "El proyectil debe ser eliminado de la lista"
        )

    def test_eliminar_enemigo(self):
        """Verifica que se eliminan enemigos correctamente."""
        gestor = GestorProyectiles(800, 600)
        enemigo = Enemigo(
            "TestEnemy", hp_max=50, ataque=10, defensa=5, tipo="terrestre"
        )
        gestor._timers_disparo_enemigo[enemigo] = 1.0

        gestor.eliminar_enemigo(enemigo)
        assert enemigo not in gestor._timers_disparo_enemigo, (
            "El enemigo debe ser eliminado del diccionario de timers"
        )

    def test_limpiar(self):
        """Verifica que se limpian todos los proyectiles y timers."""
        gestor = GestorProyectiles(800, 600)
        proyectil = Proyectil(100, 100, 0, 1, 10)
        proyectil.sprite = type("Sprite", (), {"center_x": 100, "center_y": 100})
        gestor.proyectiles.append(proyectil)
        # Not appending to lista_sprites to avoid arcade issues
        enemigo = Enemigo(
            "TestEnemy", hp_max=50, ataque=10, defensa=5, tipo="terrestre"
        )
        gestor._timers_disparo_enemigo[enemigo] = 1.0

        gestor.limpiar()
        assert len(gestor.proyectiles) == 0, "Debe limpiar la lista de proyectiles"
        assert len(gestor._timers_disparo_enemigo) == 0, (
            "Debe limpiar el diccionario de timers"
        )
        assert gestor._cooldown_jugador == 0.0, "El cooldown del jugador debe ser 0"
