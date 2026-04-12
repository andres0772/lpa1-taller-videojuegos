class SistemaExperiencia:
    """Sistema para manejar experiencia y nivelación."""

    # Experiencia base para nivel 1
    EXP_BASE = 100
    # Multiplicador para siguiente nivel
    MULT_NIVEL = 1.5

    @staticmethod
    def experiencia_para_nivel(nivel: int) -> int:
        """Calcula la experiencia necesaria para un nivel."""
        return int(
            SistemaExperiencia.EXP_BASE * (SistemaExperiencia.MULT_NIVEL ** (nivel - 1))
        )

    @staticmethod
    def puede_subir_nivel(nivel_actual: int, experiencia_actual: int) -> bool:
        """Verifica si el personaje puede subir de nivel."""
        return experiencia_actual >= SistemaExperiencia.experiencia_para_nivel(
            nivel_actual
        )

    @staticmethod
    def nivel_por_experiencia(experiencia: int) -> int:
        """Calcula el nivel basado en experiencia total."""
        nivel = 1
        while SistemaExperiencia.experiencia_para_nivel(nivel + 1) <= experiencia:
            nivel += 1
        return nivel
