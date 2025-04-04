from .base import BaseAPI
from typing import Optional, Dict

class RegistroClient(BaseAPI):
    async def crear_registro(self, data: Dict) -> Optional[Dict]:
        return await self._request("POST", "/api/registros/", json=data)

    async def obtener_registros(self, skip: int = 0, limit: int = 10) -> Optional[Dict]:
        return await self._request("GET", "/api/registros/", params={"skip": skip, "limit": limit})

    async def obtener_registro(self, registro_id: int) -> Optional[Dict]:
        return await self._request("GET", f"/api/registros/{registro_id}")

    async def actualizar_registro(self, registro_id: int, data: Dict) -> Optional[Dict]:
        return await self._request("PUT", f"/api/registros/{registro_id}", json=data)

    async def eliminar_registro(self, registro_id: int) -> Optional[Dict]:
        return await self._request("DELETE", f"/api/registros/{registro_id}")