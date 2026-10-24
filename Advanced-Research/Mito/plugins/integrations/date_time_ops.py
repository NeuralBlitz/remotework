"""
Date/Time Operations Plugin
Current time, parsing, formatting, timezone conversion, and duration calculations.
"""
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.date_time_ops")


def datetime_now_cmd(format: str = "%Y-%m-%d %H:%M:%S", timezone: str = "UTC") -> Dict:
    if timezone == "UTC":
        now = datetime.now(timezone.utc)
    else:
        offset = __import__("pytz").timezone(timezone).utcoffset(datetime.now())
        now = datetime.now() + offset
    return {"timestamp": now.timestamp(), "iso": now.isoformat(), "formatted": now.strftime(format), "timezone": timezone}


def datetime_parse_cmd(date_str: str = "", format: str = "%Y-%m-%d", source_tz: str = "UTC") -> Dict:
    dt = datetime.strptime(date_str, format)
    if source_tz != "UTC":
        dt = dt.replace(tzinfo=__import__("pytz").timezone(source_tz))
    return {"timestamp": dt.timestamp(), "iso": dt.isoformat(), "weekday": dt.strftime("%A"), "unix": int(dt.timestamp())}


def datetime_format_cmd(timestamp: float = 0, format: str = "%Y-%m-%d %H:%M:%S", timezone: str = "UTC") -> Dict:
    if not timestamp:
        timestamp = datetime.now().timestamp()
    dt = datetime.fromtimestamp(float(timestamp), tz=__import__("pytz").timezone(timezone) if timezone != "UTC" else timezone.utc)
    return {"formatted": dt.strftime(format), "iso": dt.isoformat(), "timestamp": float(timestamp)}


def datetime_timezone_convert_cmd(timestamp: float = 0, from_tz: str = "UTC", to_tz: str = "America/New_York") -> Dict:
    import pytz
    dt = datetime.fromtimestamp(float(timestamp), tz=pytz.timezone(from_tz))
    converted = dt.astimezone(pytz.timezone(to_tz))
    return {"from": {"tz": from_tz, "time": str(dt)}, "to": {"tz": to_tz, "time": str(converted)}, "unix": int(converted.timestamp())}


def datetime_duration_cmd(start: str = "", end: str = "", unit: str = "seconds") -> Dict:
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    delta = end_dt - start_dt
    units = {"seconds": delta.total_seconds(), "minutes": delta.total_seconds() / 60, "hours": delta.total_seconds() / 3600, "days": delta.days}
    return {"duration": units.get(unit, delta.total_seconds()), "unit": unit, "days": delta.days, "seconds": delta.total_seconds()}


def datetime_add_cmd(date_str: str = "", days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> Dict:
    dt = datetime.fromisoformat(date_str)
    td = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    result = dt + td
    return {"original": date_str, "result": result.isoformat(), "unix": int(result.timestamp())}


def datetime_isoweek_cmd(year: int = 0, week: int = 0, day: int = 1) -> Dict:
    from datetime import date
    if not year:
        year = datetime.now().year
    d = date.fromisocalendar(year, week or 1, day)
    return {"date": str(d), "year": year, "week": week or 1, "day": day, "weekday": d.strftime("%A")}


def register(plugin):
    plugin.register_command("now", datetime_now_cmd)
    plugin.register_command("parse", datetime_parse_cmd)
    plugin.register_command("format", datetime_format_cmd)
    plugin.register_command("timezone_convert", datetime_timezone_convert_cmd)
    plugin.register_command("duration", datetime_duration_cmd)
    plugin.register_command("add", datetime_add_cmd)
    plugin.register_command("isoweek", datetime_isoweek_cmd)


PLUGIN_METADATA = {
    "name": "date_time_ops", "version": "1.0.0",
    "description": "Date/time parsing, formatting, timezone conversion, and duration calculations",
    "author": "Mito Team", "license": "MIT",
    "tags": ["datetime", "time", "timezone", "utilities"],
    "dependencies": ["pytz"], "permissions": [],
    "min_mito_version": "1.0.1",
}

date_time_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
