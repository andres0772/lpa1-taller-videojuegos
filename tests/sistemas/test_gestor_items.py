"""
Tests unitarios para GestorItems.

PATRÓN: Tests unitarios sin dependencia de arcade usando mocks.
"""

import pytest
from src.sistemas.gestor_items import GestorItems
from src.entidades.personaje import Personaje
from src.items.item import Tesoro
from src.items.trampa import TrampaExplosiva


class TestGestorItems:
    """Tests para la clase GestorItems."""

    def test_inicializacion(self):
        """Verifica que el gestor de items se inicializa correctamente."""
        gestor = GestorItems()
        # El gestor no tiene atributos de instancia adicionales en __init__
        # Solo verifica que se crea sin errores
        assert gestor is not None, "El gestor debe crearse correctamente"

    def test_procesar_tesoro(self):
        """Verifica que al procesar un tesoro se agrega oro al personaje."""
        gestor = GestorItems()

        # Crear personaje (stats por defecto: HP=100, ataque=10, defensa=5)
        personaje = Personaje(nombre="Hero")

        # No hay forma de inicializar oro directamente, es 0 por defecto
        # Verificar oro inicial
        assert personaje._oro == 0, "El oro debe iniciar en 0"

        # Crear tesoro
        tesoro = Tesoro(nombre="Bolsa de Oro", valor=50, precio=0)

        # Simular listas vacías (como si el item ya fue procesado)
        items = []
        lista_sprites = []

        # Procesar tesoro (método directo sin arcade)
        oro_ganado = gestor.procesar_tesoro(personaje, tesoro, items, lista_sprites)

        # Verificar que se retornó el valor correcto
        assert oro_ganado == 50, "Debe retornar 50 de oro"

        # Verificar que el personaje recibió el oro
        assert personaje._oro == 50, "El personaje debe tener 50 oro más"

    def test_procesar_trampa(self):
        """Verifica que al procesar una trampa se aplica daño al personaje."""
        gestor = GestorItems()

        # Crear personaje con HP por defecto (100)
        personaje = Personaje(nombre="Hero")
        hp_inicial = personaje.hp_actual

        # Crear trampa
        trampa = TrampaExplosiva(nombre="Bomba", daño=30, alcance=50)

        # Simular listas vacías (como si el item ya fue procesado)
        items = []
        lista_sprites = []

        # Procesar trampa (método directo sin arcade)
        daño_recibido = gestor.procesar_trampa(personaje, trampa, items, lista_sprites)

        # Verificar que se retornó el daño correcto
        assert daño_recibido == 30, "Debe retornar 30 de daño"

        # Verificar que el personaje recibió el daño
        assert personaje.hp_actual == hp_inicial - 30, "El personaje debe perder 30 HP"

    def test_procesar_tesoro_multiple(self):
        """Verifica el procesamiento de múltiples tesoros acumulados."""
        gestor = GestorItems()

        # Crear personaje
        personaje = Personaje(nombre="Hero")

        # Procesar primer tesoro
        tesoro1 = Tesoro(nombre="Moneda", valor=10, precio=0)
        items = []
        lista_sprites = []
        gestor.procesar_tesoro(personaje, tesoro1, items, lista_sprites)

        # Procesar segundo tesoro
        tesoro2 = Tesoro(nombre="Bolsa", valor=25, precio=0)
        gestor.procesar_tesoro(personaje, tesoro2, items, lista_sprites)

        # Verificar oro total
        assert personaje._oro == 35, "El personaje debe tener 35 oro en total"

    def test_procesar_trampa_no_mata_mas_de_lo_que_tiene(self):
        """Verifica que el daño no hace HP negativo."""
        gestor = GestorItems()

        # Crear personaje con poco HP
        personaje = Personaje(nombre="Hero")
        personaje._hp_actual = 10  # HP bajo intencionalmente

        # Crear trampa con daño grande
        trampa = TrampaExplosiva(nombre="Bomba", daño=100, alcance=50)

        items = []
        lista_sprites = []
        gestor.procesar_trampa(personaje, trampa, items, lista_sprites)

        # Verificar que HP no es negativo (recibir_daño usa max(0, ...))
        assert personaje.hp_actual >= 0, "El HP no debe ser negativo"

    def test_procesar_tesoro_sin_sprite(self):
        """Verifica que procesar tesoro funciona sin sprite (caso extremo)."""
        gestor = GestorItems()

        personaje = Personaje(nombre="Hero")

        # Crear tesoro sin sprite
        tesoro = Tesoro(nombre="Tesoro", valor=100, precio=0)
        tesoro.sprite = None  # Forzar sin sprite

        items = []
        lista_sprites = []

        # Debe funcionar igual (el método no usa sprite directamente)
        oro_ganado = gestor.procesar_tesoro(personaje, tesoro, items, lista_sprites)

        assert oro_ganado == 100, "Debe retornar el valor del tesoro"
        assert personaje._oro == 100, "Debe agregar el oro"

    @pytest.mark.skip(
        reason="Requires real arcade.Sprite collision detection - integration test"
    )
    def test_verificar_colisiones(self):
        """Verifica que se detectan colisiones con items."""
        # Este test requiere sprites reales de arcade para verificar colisiones
        # Por eso se salta en tests unitarios
        pass

    @pytest.mark.skip(
        reason="Requires real arcade.Sprite collision detection - integration test"
    )
    def test_verificar_colisiones_tesoro_y_trampa(self):
        """Verifica que se procesan correctamente tesoros y trampas."""
        # Este test requiere sprites reales de arcade
        pass
