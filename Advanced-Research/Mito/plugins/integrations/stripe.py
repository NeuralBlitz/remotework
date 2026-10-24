"""
Stripe Payments Plugin
Charges, subscriptions, customers, webhooks
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.stripe")


class StripeClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("STRIPE_API_KEY", "")
        self.base_url = "https://api.stripe.com/v1"

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def _request(self, method: str, path: str, data: Dict = None) -> Any:
        import requests
        url = f"{self.base_url}{path}"
        resp = requests.request(method, url, headers=self._headers(), data=data, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def create_customer(self, email: str, name: str = "", metadata: Dict = None) -> Dict:
        data = {"email": email, "name": name}
        if metadata:
            for k, v in metadata.items():
                data[f"metadata[{k}]"] = v
        return self._request("POST", "/customers", data)

    def get_customer(self, customer_id: str) -> Dict:
        return self._request("GET", f"/customers/{customer_id}")

    def list_customers(self, limit: int = 10) -> List[Dict]:
        result = self._request("GET", f"/customers?limit={limit}")
        return result.get("data", [])

    def create_charge(self, amount: int, currency: str, customer: str = "",
                      description: str = "") -> Dict:
        data = {"amount": amount, "currency": currency}
        if customer:
            data["customer"] = customer
        if description:
            data["description"] = description
        return self._request("POST", "/charges", data)

    def create_payment_intent(self, amount: int, currency: str = "usd",
                              customer: str = "", description: str = "") -> Dict:
        data = {"amount": amount, "currency": currency}
        if customer:
            data["customer"] = customer
        if description:
            data["description"] = description
        return self._request("POST", "/payment_intents", data)

    def create_subscription(self, customer: str, price_id: str) -> Dict:
        return self._request("POST", "/subscriptions", {
            "customer": customer, "items[0][price]": price_id
        })

    def cancel_subscription(self, subscription_id: str) -> Dict:
        return self._request("DELETE", f"/subscriptions/{subscription_id}")

    def list_subscriptions(self, customer: str = "", limit: int = 10) -> List[Dict]:
        params = f"?limit={limit}"
        if customer:
            params += f"&customer={customer}"
        result = self._request("GET", f"/subscriptions{params}")
        return result.get("data", [])

    def create_product(self, name: str, description: str = "") -> Dict:
        data = {"name": name}
        if description:
            data["description"] = description
        return self._request("POST", "/products", data)

    def create_price(self, product: str, unit_amount: int, currency: str = "usd",
                     recurring: bool = False, interval: str = "month") -> Dict:
        data = {"product": product, "unit_amount": unit_amount, "currency": currency}
        if recurring:
            data["recurring[interval]"] = interval
        return self._request("POST", "/prices", data)

    def create_refund(self, charge: str, amount: int = None) -> Dict:
        data = {"charge": charge}
        if amount:
            data["amount"] = amount
        return self._request("POST", "/refunds", data)

    def list_charges(self, customer: str = "", limit: int = 10) -> List[Dict]:
        params = f"?limit={limit}"
        if customer:
            params += f"&customer={customer}"
        result = self._request("GET", f"/charges{params}")
        return result.get("data", [])

    def get_balance(self) -> Dict:
        return self._request("GET", "/balance")


def stripe_create_customer_cmd(email: str = "", name: str = "") -> Dict:
    """Create a Stripe customer."""
    client = StripeClient()
    return client.create_customer(email, name)


def stripe_create_charge_cmd(amount: int = 0, currency: str = "usd",
                              customer: str = "") -> Dict:
    """Create a Stripe charge."""
    client = StripeClient()
    return client.create_charge(amount, currency, customer)


def stripe_create_payment_cmd(amount: int = 0, currency: str = "usd") -> Dict:
    """Create a Stripe PaymentIntent."""
    client = StripeClient()
    return client.create_payment_intent(amount, currency)


def register(plugin):
    plugin.register_command("stripe_create_customer", stripe_create_customer_cmd)
    plugin.register_command("stripe_create_charge", stripe_create_charge_cmd)
    plugin.register_command("stripe_create_payment", stripe_create_payment_cmd)
    plugin.set_resource("client_class", StripeClient)


PLUGIN_METADATA = {
    "name": "stripe",
    "version": "1.0.0",
    "description": "Stripe payments - Charges, subscriptions, customers, refunds",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["stripe", "payments", "billing", "subscriptions"],
    "dependencies": [],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


stripe_plugin = {"metadata": PLUGIN_METADATA, "register": register}
