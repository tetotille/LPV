from __future__ import annotations

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno desde .env
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class DatabaseManager:
    def __init__(self) -> None:
        self._validate_config()
        try:
            self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            print(f"Error al conectar con Supabase: {e}", file=sys.stderr)
            raise RuntimeError(f"Fallo en la conexión con Supabase. Revisa tu URL y Key.\nError: {e}")

    def _validate_config(self) -> None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            msg = (
                "Error: SUPABASE_URL o SUPABASE_KEY no encontrados.\n"
                "Asegúrate de configurar el archivo .env con tus credenciales de Supabase."
            )
            print(msg, file=sys.stderr)
            # No levantamos RuntimeError aquí para que el mensaje anterior se imprima antes del traceback
            raise EnvironmentError(msg)

    def initialize(self) -> None:
        """
        No es necesario inicializar el esquema localmente para Supabase.
        """
        pass
