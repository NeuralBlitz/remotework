"""
Google Calendar Integration Plugin
Events, calendars via Google Calendar API
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.calendar")


class GoogleCalendarClient:
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.environ.get("GOOGLE_CALENDAR_TOKEN", "")
        self.base_url = "https://www.googleapis.com/calendar/v3"

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, data: Dict = None, params: Dict = None) -> Any:
        import requests
        url = f"{self.base_url}{path}"
        resp = requests.request(method, url, headers=self._headers(), json=data, params=params, timeout=30)
        resp.raise_for_status()
        if resp.status_code == 204:
            return {"ok": True}
        return resp.json()

    def list_calendars(self) -> List[Dict]:
        result = self._request("GET", "/users/me/calendarList")
        return result.get("items", [])

    def get_events(self, calendar_id: str = "primary", time_min: str = None,
                   time_max: str = None, max_results: int = 50) -> List[Dict]:
        params = {"maxResults": max_results, "singleEvents": True, "orderBy": "startTime"}
        if time_min:
            params["timeMin"] = time_min
        else:
            params["timeMin"] = datetime.utcnow().isoformat() + "Z"
        if time_max:
            params["timeMax"] = time_max
        result = self._request("GET", f"/calendars/{calendar_id}/events", params=params)
        return result.get("items", [])

    def create_event(self, calendar_id: str = "primary", summary: str = "",
                     description: str = "", location: str = "",
                     start_time: str = "", end_time: str = "",
                     attendees: List[str] = None, timezone: str = "UTC") -> Dict:
        payload = {
            "summary": summary,
            "description": description,
            "location": location,
            "start": {"dateTime": start_time, "timeZone": timezone},
            "end": {"dateTime": end_time, "timeZone": timezone},
        }
        if attendees:
            payload["attendees"] = [{"email": a} for a in attendees]
        return self._request("POST", f"/calendars/{calendar_id}/events", payload)

    def update_event(self, event_id: str, calendar_id: str = "primary", **kwargs) -> Dict:
        return self._request("PATCH", f"/calendars/{calendar_id}/events/{event_id}", kwargs)

    def delete_event(self, event_id: str, calendar_id: str = "primary") -> Dict:
        return self._request("DELETE", f"/calendars/{calendar_id}/events/{event_id}")

    def quick_add(self, text: str, calendar_id: str = "primary") -> Dict:
        params = {"text": text}
        return self._request("POST", f"/calendars/{calendar_id}/events/quickAdd", params=params)

    def get_event(self, event_id: str, calendar_id: str = "primary") -> Dict:
        return self._request("GET", f"/calendars/{calendar_id}/events/{event_id}")

    def get_today_events(self, calendar_id: str = "primary") -> List[Dict]:
        now = datetime.utcnow()
        start = now.replace(hour=0, minute=0, second=0).isoformat() + "Z"
        end = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0).isoformat() + "Z"
        return self.get_events(calendar_id, time_min=start, time_max=end)


def calendar_list_cmd() -> List[Dict]:
    """List Google Calendars."""
    client = GoogleCalendarClient()
    return client.list_calendars()


def calendar_events_cmd(calendar_id: str = "primary", max_results: int = 20) -> List[Dict]:
    """Get upcoming events from a Google Calendar."""
    client = GoogleCalendarClient()
    return client.get_events(calendar_id, max_results=max_results)


def calendar_today_cmd(calendar_id: str = "primary") -> List[Dict]:
    """Get today's events from a Google Calendar."""
    client = GoogleCalendarClient()
    return client.get_today_events(calendar_id)


def calendar_create_cmd(summary: str = "", start_time: str = "", end_time: str = "") -> Dict:
    """Create a Google Calendar event."""
    client = GoogleCalendarClient()
    return client.create_event(summary=summary, start_time=start_time, end_time=end_time)


def register(plugin):
    plugin.register_command("calendar_list", calendar_list_cmd)
    plugin.register_command("calendar_events", calendar_events_cmd)
    plugin.register_command("calendar_today", calendar_today_cmd)
    plugin.register_command("calendar_create", calendar_create_cmd)
    plugin.set_resource("client_class", GoogleCalendarClient)


PLUGIN_METADATA = {
    "name": "calendar",
    "version": "1.0.0",
    "description": "Google Calendar integration - Events, calendars, scheduling",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["calendar", "google", "events", "scheduling"],
    "dependencies": [],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


calendar_plugin = {
    "metadata": PLUGIN_METADATA,
    "register": register,
}
