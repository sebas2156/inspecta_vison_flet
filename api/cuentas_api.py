from .base import BaseAPI
from typing import Optional, Dict

class CuentaClient(BaseAPI):
    async def crear_cuenta(self, data: Dict) -> Optional[Dict]:
        return await self._request("POST", "/api/cuentas/", json=data)

    async def obtener_cuentas(self, skip: int = 0, limit: int = 10) -> Optional[Dict]:
        return await self._request("GET", "/api/cuentas/", params={"skip": skip, "limit": limit})

    async def obtener_cuenta(self, cuenta_id: int) -> Optional[Dict]:
        return await self._request("GET", f"/api/cuentas/{cuenta_id}")

    async def actualizar_cuenta(self, cuenta_id: int, data: Dict) -> Optional[Dict]:
        return await self._request("PUT", f"/api/cuentas/{cuenta_id}", json=data)

    async def eliminar_cuenta(self, cuenta_id: int) -> Optional[Dict]:
        return await self._request("DELETE", f"/api/cuentas/{cuenta_id}")