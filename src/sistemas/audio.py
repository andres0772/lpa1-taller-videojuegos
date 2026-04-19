"""
Sistema de audio centralizado para el juego.

Gestiona la carga y reproducción de efectos de sonido usando Arcade.
Implementa el patrón singleton para tener una única instancia global.
"""

import arcade
import os


class GestorAudio:
    """
    Gestor centralizado de sonidos del juego.

    Usa el patrón singleton para mantener una única instancia global.
    Carga los sonidos desde assets/audio/ y expone métodos simples
    para reproducirlos.
    """

    _instancia = None

    _sonido_disparo = None
    _sonido_recompensa = None
    _sonido_victoria = None
    _sonido_ui = None

    def __init__(self):
        """Inicializa el gestor cargando todos los sonidos."""
        # Calcular la ruta base a assets/audio
        # Subimos 3 niveles desde src/sistemas/audio.py
        base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "assets",
            "audio"
        )

        # Cargar sonidos con manejo de errores
        self._sonido_disparo = self._cargar_sonido(base_path, "disparo.wav")
        self._sonido_recompensa = self._cargar_sonido(base_path, "recompensa.wav")
        self._sonido_victoria = self._cargar_sonido(base_path, "win.wav")
        self._sonido_ui = self._cargar_sonido(base_path, "UI.wav")

    def _cargar_sonido(self, base_path: str, archivo: str) -> arcade.Sound | None:
        """
        Carga un sonido desde archivo con manejo de errores.

        Args:
            base_path: Ruta base al directorio de audio
            archivo: Nombre del archivo de sonido

        Returns:
            El objeto Sound cargado o None si falló
        """
        try:
            ruta = os.path.join(base_path, archivo)
            return arcade.Sound(ruta)
        except Exception as e:
            print(f"[GestorAudio] No se pudo cargar sonido '{archivo}': {e}")
            return None

    @classmethod
    def obtener(cls) -> "GestorAudio":
        """
        Obtiene la instancia única del gestor de audio.

        Returns:
            La instancia singleton de GestorAudio
        """
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def _reproducir(self, nombre_sonido: str) -> None:
        """
        Reproduce un sonido por su nombre de atributo.

        Args:
            nombre_sonido: Nombre del atributo que contiene el sonido
        """
        sonido = getattr(self, nombre_sonido, None)
        if sonido is not None:
            arcade.play_sound(sonido)

    @staticmethod
    def reproducir_disparo() -> None:
        """Reproduce el sonido de disparo."""
        GestorAudio.obtener()._reproducir("_sonido_disparo")

    @staticmethod
    def reproducir_recompensa() -> None:
        """Reproduce el sonido de recompensa."""
        GestorAudio.obtener()._reproducir("_sonido_recompensa")

    @staticmethod
    def reproducir_victoria() -> None:
        """Reproduce el sonido de victoria."""
        GestorAudio.obtener()._reproducir("_sonido_victoria")

    @staticmethod
    def reproducir_ui() -> None:
        """Reproduce el sonido de UI."""
        GestorAudio.obtener()._reproducir("_sonido_ui")
