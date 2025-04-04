from .base import BaseAPI
from typing import Optional, Dict

class RegionClient(BaseAPI):
    async def crear_region(self, data: Dict) -> Optional[Dict]:
        return await self._request("POST", "/api/regiones/", json=data)

    async def obtener_regiones(self, skip: int = 0, limit: int = 10) -> Optional[Dict]:
        return await self._request("GET", "/api/regiones/", params={"skip": skip, "limit": limit})

    async def obtener_region(self, region_id: int) -> Optional[Dict]:
        return await self._request("GET", f"/api/regiones/{region_id}")

    async def actualizar_region(self, region_id: int, data: Dict) -> Optional[Dict]:
        return await self._request("PUT", f"/api/regiones/{region_id}", json=data)

    async def eliminar_region(self, region_id: int) -> Optional[Dict]:
        return await self._request("DELETE", f"/api/regiones/{region_id}")