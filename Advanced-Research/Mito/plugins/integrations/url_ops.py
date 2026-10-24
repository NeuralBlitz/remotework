"""
URL Operations Plugin
Parse, build, encode, decode, and shorten URLs.
"""
import logging
from urllib.parse import parse_qs, quote, unquote, urlencode, urljoin, urlparse, urlunparse

logger = logging.getLogger("mito.plugins.url_ops")


def url_parse_cmd(url: str = "") -> Dict:
    parsed = urlparse(url)
    return {
        "scheme": parsed.scheme, "netloc": parsed.netloc, "hostname": parsed.hostname,
        "port": parsed.port, "path": parsed.path, "params": parsed.params,
        "query": dict(parse_qs(parsed.query)), "fragment": parsed.fragment,
    }


def url_build_cmd(scheme: str = "https", hostname: str = "", path: str = "/",
                  params: str = "", query: str = "", fragment: str = "") -> str:
    query_dict = dict(parse_qs(query)) if query else {}
    return urlunparse((scheme, hostname, path, params, urlencode(query_dict), fragment))


def url_encode_cmd(text: str = "", safe: str = "") -> str:
    return quote(text, safe=safe)


def url_decode_cmd(text: str = "") -> str:
    return unquote(text)


def url_encode_params_cmd(params: str = "") -> str:
    import json
    d = json.loads(params) if params.startswith("{") else {k.strip(): v.strip() for k, v in (p.split("=") for p in params.split("&")) if "=" in p}
    return urlencode(d)


def url_join_cmd(base: str = "", relative: str = "") -> str:
    return urljoin(base, relative)


def url_get_params_cmd(url: str = "") -> Dict:
    parsed = urlparse(url)
    return {"params": parse_qs(parsed.query), "keys": list(parse_qs(parsed.query).keys())}


def url_sanitize_cmd(url: str = "") -> str:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return ""
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))


def url_is_valid_cmd(url: str = "") -> Dict:
    try:
        result = urlparse(url)
        return {"valid": all([result.scheme, result.netloc]), "scheme": result.scheme, "hostname": result.hostname}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def register(plugin):
    plugin.register_command("parse", url_parse_cmd)
    plugin.register_command("build", url_build_cmd)
    plugin.register_command("encode", url_encode_cmd)
    plugin.register_command("decode", url_decode_cmd)
    plugin.register_command("encode_params", url_encode_params_cmd)
    plugin.register_command("join", url_join_cmd)
    plugin.register_command("get_params", url_get_params_cmd)
    plugin.register_command("sanitize", url_sanitize_cmd)
    plugin.register_command("is_valid", url_is_valid_cmd)


PLUGIN_METADATA = {
    "name": "url_ops", "version": "1.0.0",
    "description": "URL parsing, building, encoding, and validation",
    "author": "Mito Team", "license": "MIT",
    "tags": ["url", "web", "encoding", "utilities"],
    "dependencies": [], "permissions": [],
    "min_mito_version": "1.0.1",
}

url_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
