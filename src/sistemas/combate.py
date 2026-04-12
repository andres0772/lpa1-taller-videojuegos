from typing import NamedTuple
from ..entidades.entidad import Entidad


class ResultadoCombate(NamedTuple):
    dano_infligido: int
    dano_recibido: int
    enemigo_derrotado: bool


class SistemaCombate:
    """Sistema para calcular y resolver combate."""

    @staticmethod
    def _obtener_ataque_total(entidad: Entidad) -> int:
        """Obtiene el ataque total (incluyendo equipamiento si está disponible)."""
        if hasattr(entidad, "ataque_total"):
            return entidad.ataque_total
        return entidad.ataque

    @staticmethod
    def _obtener_defensa_total(entidad: Entidad) -> int:
        """Obtiene la defensa total (incluyendo equipamiento si está disponible)."""
        if hasattr(entidad, "defensa_total"):
            return entidad.defensa_total
        return entidad.defensa

    @staticmethod
    def calcular_daño(ataque: int, defensa: int) -> int:
        """Calcula el daño base después de aplicar defensa."""
        dano_base = ataque - (defensa // 2)
        return max(1, dano_base)

    @staticmethod
    def atacar(atacante: Entidad, defensor: Entidad) -> ResultadoCombate:
        """Ejecuta un ataque y retorna el resultado."""
        # Usar stats totales si están disponibles (para Personaje con equipamiento)
        ataque_atacante = SistemaCombate._obtener_ataque_total(atacante)
        defensa_defensor = SistemaCombate._obtener_defensa_total(defensor)

        dano = SistemaCombate.calcular_daño(ataque_atacante, defensa_defensor)
        defensor.recibir_daño(dano)

        # Contraataca si sigue vivo
        dano_recibido = 0
        if defensor.esta_vivo():
            ataque_defensor = SistemaCombate._obtener_ataque_total(defensor)
            defensa_atacante = SistemaCombate._obtener_defensa_total(atacante)
            dano_recibido = SistemaCombate.calcular_daño(
                ataque_defensor, defensa_atacante
            )
            atacante.recibir_daño(dano_recibido)

        return ResultadoCombate(
            dano_infligido=dano,
            dano_recibido=dano_recibido,
            enemigo_derrotado=not defensor.esta_vivo(),
        )
