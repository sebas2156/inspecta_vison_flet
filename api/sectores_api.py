from .base import BaseAPI
from typing import Optional, Dict

class SectorClient(BaseAPI):
    async def crear_sector(self, data: Dict) -> Optional[Dict]:
        return await self._request("POST", "/api/sectores/", json=data)

    async def obtener_sectores(self, skip: int = 0, limit: int = 10) -> Optional[Dict]:
        return await self._request("GET", "/api/sectores/", params={"skip": skip, "limit": limit})

    async def obtener_sector(self, sector_id: int) -> Optional[Dict]:
        return await self._request("GET", f"/api/sectores/{sector_id}")

    async def actualizar_sector(self, sector_id: int, data: Dict) -> Optional[Dict]:
        return await self._request("PUT", f"/api/sectores/{sector_id}", json=data)

    async def eliminar_sector(self, sector_id: int) -> Optional[Dict]:
        return await self._request("DELETE", f"/api/sectores/{sector_id}")