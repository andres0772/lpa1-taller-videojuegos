from typing import NamedTuple
from ..entidades.entidad import Entidad


class ResultadoCombate(NamedTuple):
    dano_infligido: int
    dano_recibido: int
    enemigo_derrotado: bool


class SistemaCombate:
    """Sistema para calcular y resolver combate."""

    @staticmethod
    def calcular_daño(ataque: int, defensa: int) -> int:
        """Calcula el daño base después de aplicar defensa."""
        dano_base = ataque - (defensa // 2)
        return max(1, dano_base)

    @staticmethod
    def atacar(atacante: Entidad, defensor: Entidad) -> ResultadoCombate:
        """Ejecuta un ataque y retorna el resultado."""
        dano = SistemaCombate.calcular_daño(atacante.ataque, defensor.defensa)
        defensor.recibir_daño(dano)

        # Contraataca si sigue vivo
        dano_recibido = 0
        if defensor.esta_vivo():
            dano_recibido = SistemaCombate.calcular_daño(
                defensor.ataque, atacante.defensa
            )
            atacante.recibir_daño(dano_recibido)

        return ResultadoCombate(
            dano_infligido=dano,
            dano_recibido=dano_recibido,
            enemigo_derrotado=not defensor.esta_vivo(),
        )
