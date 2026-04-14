"""
Tests unitarios para GestorCombate.

PATRÓN: Tests unitarios sin dependencia de arcade usando mocks.
"""

import pytest
from src.sistemas.gestor_combate import GestorCombate
from src.entidades.personaje import Personaje
from src.entidades.enemigo import Enemigo


class TestGestorCombate:
    """Tests para la clase GestorCombate."""

    def test_inicializacion(self):
        """Verifica que el gestor de combate se inicializa correctamente."""
        gestor = GestorCombate()
        assert gestor._cooldown == 0.0, "El cooldown debe inicializar en 0.0"
        assert gestor.COOLDOWN_COMBATE == 1.0, (
            "El cooldown de combate debe ser 1.0 segundo"
        )

    def test_puede_combatir(self):
        """Verifica que el jugador puede combatir cuando el cooldown está en 0."""
        gestor = GestorCombate()

        # Cooldown en 0 = puede combatir
        assert gestor.puede_combatir, (
            "El jugador debe poder combatir cuando el cooldown está en 0"
        )

        # Cooldown activo = no puede combatir
        gestor._cooldown = 1.0
        assert not gestor.puede_combatir, (
            "El jugador no debe poder combatir cuando el cooldown está activo"
        )

        # Cooldown negativo (ya expiró) = puede combatir
        gestor._cooldown = -0.1
        assert gestor.puede_combatir, (
            "El jugador debe poder combatir cuando el cooldown ya expiró (negativo)"
        )

    def test_actualizar_cooldown(self):
        """Verifica que el cooldown disminuye correctamente con el tiempo."""
        gestor = GestorCombate()

        # Inicializar cooldown
        gestor._cooldown = 1.0
        gestor.actualizar_cooldown(0.5)
        assert gestor._cooldown == 0.5, "El cooldown debe reducirse en 0.5 segundos"

        # Reducir a cero
        gestor.actualizar_cooldown(0.5)
        assert gestor._cooldown == 0.0, "El cooldown debe llegar a cero"

        # No debe ser negativo (protección con max())
        gestor._cooldown = 0.5
        gestor.actualizar_cooldown(1.0)
        assert gestor._cooldown == 0.0, "El cooldown no debe ser negativo (usar max())"

    def test_no_combate_en_cooldown(self):
        """Verifica que no se puede combatir mientras el cooldown está activo."""
        gestor = GestorCombate()

        # Activar cooldown
        gestor._cooldown = 0.5

        # Verificar que no puede combatix (la propiedad retorna False)
        assert not gestor.puede_combatir, "No debe poder combatir con cooldown activo"

    @pytest.mark.skip(
        reason="Requires real arcade.Sprite collision detection - integration test"
    )
    def test_verificar_combate(self):
        """Verifica que se detectan colisiones con enemigos y se ejecuta combate."""
        # Este test requiere sprites reales de arcade para verificar colisiones
        # Por eso se salta en tests unitarios
        pass

    def test_constantes_configuracion(self):
        """Verifica las constantes de configuración del gestor."""
        gestor = GestorCombate()

        # Verificar que las constantes son las esperadas
        assert hasattr(gestor, "COOLDOWN_COMBATE"), (
            "Debe tener constante COOLDOWN_COMBATE"
        )
        assert isinstance(gestor.COOLDOWN_COMBATE, (int, float)), (
            "COOLDOWN_COMBATE debe ser numérico"
        )
