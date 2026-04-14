from __future__ import annotations

from typing import Any

from ..db.database import DatabaseManager
from ..utils.date_utils import normalize_date


class RecordService:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db
        # No es necesario inicializar el esquema para Supabase en el servicio
        pass

    def _map_row(self, row: dict[str, Any]) -> dict[str, Any]:
        """Maps Supabase columns to UI expected names."""
        return {
            "id": row.get("id"),
            "date_obs": str(row.get("date_obs")) if row.get("date_obs") else "",
            "noaa": row.get("noaa"),
            "z_class": row.get("z_class"),
            "p_class": row.get("p_class"),
            "c_class": row.get("c_class"),
            "mcintosh_full": row.get("mcintosh_full"),
            "latitude": row.get("lat"),
            "longitude": row.get("lon"),
            "area": row.get("area"),
            "num_spots": row.get("num_spots_srs"),
            "mag_class": row.get("mag_class"),
        }

    def list_dates(self) -> list[str]:
        """Fetch unique observation dates sorted descending."""
        # Usamos rpc() para una consulta más eficiente si estuviera disponible, 
        # pero por ahora hacemos un select de una columna.
        response = self.db.client.table("sunspot_crops").select("date_obs").execute()
        
        # Procesar en Python para obtener valores únicos únicos (Postgrest select no tiene DISTINCT directo fácilmente)
        dates = sorted(list(set(str(row["date_obs"]) for row in response.data if row.get("date_obs"))), reverse=True)
        return dates

    def get_all_records(self) -> list[dict[str, Any]]:
        """Fetch the most recent 500 records."""
        response = (
            self.db.client.table("sunspot_crops")
            .select("*")
            .order("date_obs", desc=True)
            .limit(500)
            .execute()
        )
        return [self._map_row(row) for row in response.data]

    def get_records_by_date(self, date_obs: str) -> list[dict[str, Any]]:
        """Fetch records for a specific date."""
        try:
            date_obs = normalize_date(date_obs)
        except ValueError:
            return []
            
        response = (
            self.db.client.table("sunspot_crops")
            .select("*")
            .eq("date_obs", date_obs)
            .order("noaa")
            .execute()
        )
        return [self._map_row(row) for row in response.data]
