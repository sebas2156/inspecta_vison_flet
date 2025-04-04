from .base import BaseAPI
from typing import Optional, Dict

class ProductoClient(BaseAPI):
    async def crear_producto(self, data: Dict) -> Optional[Dict]:
        return await self._request("POST", "/api/productos/", json=data)

    async def obtener_productos(self, skip: int = 0, limit: int = 10) -> Optional[Dict]:
        return await self._request("GET", "/api/productos/", params={"skip": skip, "limit": limit})

    async def obtener_producto(self, producto_codigo: str) -> Optional[Dict]:
        return await self._request("GET", f"/api/productos/{producto_codigo}")

    async def actualizar_producto(self, producto_codigo: str, data: Dict) -> Optional[Dict]:
        return await self._request("PUT", f"/api/productos/{producto_codigo}", json=data)

    async def eliminar_producto(self, producto_codigo: str) -> Optional[Dict]:
        return await self._request("DELETE", f"/api/productos/{producto_codigo}")