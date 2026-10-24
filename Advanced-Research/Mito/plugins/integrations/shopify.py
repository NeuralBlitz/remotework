"""
Shopify E-commerce Plugin
Products, orders, customers via REST Admin API
"""
import os
from typing import Dict, List

class ShopifyClient:
    def __init__(self, shop: str = None, token: str = None):
        self.shop = shop or os.environ.get("SHOPIFY_SHOP", "")
        self.token = token or os.environ.get("SHOPIFY_TOKEN", "")
        self.base_url = f"https://{self.shop}.myshopify.com/admin/api/2024-01"

    def _headers(self) -> Dict[str, str]:
        return {"X-Shopify-Access-Token": self.token, "Content-Type": "application/json"}

    def list_products(self, limit: int = 50) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/products.json", headers=self._headers(), params={"limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("products", [])

    def create_product(self, title: str, body_html: str = "", variants: List[Dict] = None) -> Dict:
        import requests
        payload = {"product": {"title": title, "body_html": body_html}}
        if variants:
            payload["product"]["variants"] = variants
        resp = requests.post(f"{self.base_url}/products.json", headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_orders(self, status: str = "any", limit: int = 50) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/orders.json", headers=self._headers(), params={"status": status, "limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("orders", [])

    def get_order(self, order_id: int) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/orders/{order_id}.json", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_customers(self, limit: int = 50) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/customers.json", headers=self._headers(), params={"limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("customers", [])

    def create_customer(self, email: str, first_name: str = "", last_name: str = "") -> Dict:
        import requests
        payload = {"customer": {"email": email, "first_name": first_name, "last_name": last_name}}
        resp = requests.post(f"{self.base_url}/customers.json", headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def inventory_levels(self, location_id: int = None) -> List[Dict]:
        import requests
        params = {}
        if location_id:
            params["location_ids"] = location_id
        resp = requests.get(f"{self.base_url}/inventory_levels.json", headers=self._headers(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("inventory_levels", [])

def register(plugin):
    plugin.set_resource("client_class", ShopifyClient)

shopify_plugin = {
    "metadata": {"name": "shopify", "version": "1.0.0", "description": "Shopify e-commerce - Products, orders, customers",
                 "author": "Mito Team", "license": "MIT", "tags": ["shopify", "ecommerce", "products", "orders"],
                 "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"},
    "register": register,
}
