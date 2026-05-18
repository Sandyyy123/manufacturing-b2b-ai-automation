import os
import httpx
from typing import Optional, Dict, Any
from enum import Enum


class ERPSystem(str, Enum):
    SAP = "sap"
    HUBSPOT = "hubspot"
    SALESFORCE = "salesforce"
    MOCK = "mock"


class ERPConnector:
    def __init__(self, system: ERPSystem = ERPSystem.MOCK):
        self.system = system
        self.base_url = os.getenv(f"{system.value.upper()}_BASE_URL", "")
        self.api_key = os.getenv(f"{system.value.upper()}_API_KEY", "")

    async def get_customer(self, customer_id: str) -> Dict[str, Any]:
        if self.system == ERPSystem.MOCK:
            return {"id": customer_id, "name": "Demo Customer GmbH", "tier": "standard",
                    "credit_limit": 50000, "payment_terms": "net30"}
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}/customers/{customer_id}",
                                 headers={"Authorization": f"Bearer {self.api_key}"})
            r.raise_for_status()
            return r.json()

    async def create_quote(self, customer_id: str, quote_data: dict) -> Dict[str, Any]:
        if self.system == ERPSystem.MOCK:
            import uuid
            return {"quote_id": f"QT-{str(uuid.uuid4())[:8].upper()}", "status": "draft",
                    "customer_id": customer_id}
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{self.base_url}/quotes",
                                  json={"customer_id": customer_id, **quote_data},
                                  headers={"Authorization": f"Bearer {self.api_key}"})
            r.raise_for_status()
            return r.json()

    async def sync_order(self, order_data: dict) -> Dict[str, Any]:
        if self.system == ERPSystem.MOCK:
            return {"synced": True, "erp_ref": f"ERP-{order_data.get('order_id', 'NEW')}"}
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{self.base_url}/orders", json=order_data,
                                  headers={"Authorization": f"Bearer {self.api_key}"})
            r.raise_for_status()
            return r.json()
