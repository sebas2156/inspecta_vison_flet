from .base import BaseAPI
from typing import Optional, Dict, List

class CamaraClient(BaseAPI):
    async def crear_camara(self, data: Dict) -> Optional[Dict]:
        return await self._request("POST", "/api/camaras/", json=data)

    async def obtener_camaras(self, skip: int = 0, limit: int = 10) -> Optional[Dict]:
        return await self._request("GET", "/api/camaras/", params={"skip": skip, "limit": limit})

    async def obtener_camara(self, camara_id: int) -> Optional[Dict]:
        return await self._request("GET", f"/api/camaras/{camara_id}")

    async def actualizar_camara(self, camara_id: int, data: Dict) -> Optional[Dict]:
        return await self._request("PUT", f"/api/camaras/{camara_id}", json=data)

    async def eliminar_camara(self, camara_id: int) -> Optional[Dict]:
        return await self._request("DELETE", f"/api/camaras/{camara_id}")