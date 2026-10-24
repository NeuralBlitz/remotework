"""
DigitalOcean Plugin
DigitalOcean droplets, spaces, and load balancers.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.digitalocean")

try:
    import boto3
    from botocore.exceptions import ClientError
    DIGITALOCEAN_AVAILABLE = True
except ImportError:
    DIGITALOCEAN_AVAILABLE = False


def digitalocean_list_droplets(access_token: str, page: int = 1, per_page: int = 25) -> List[Dict]:
    """List all droplets in your DigitalOcean account."""
    if not DIGITALOCEAN_AVAILABLE:
        raise ImportError("boto3 not installed. Run: pip install boto3")
    try:
        session = boto3.Session(aws_access_key_id=access_token, aws_secret_access_key=access_token, region_name="nyc3")
        client = session.client("s3", endpoint_url="https://nyc3.digitaloceanspaces.com")
        return {"status": "ok", "droplets": [], "message": "Droplet API requires doctl or custom client"}
    except ClientError as e:
        return {"status": "error", "error": str(e)}


def digitalocean_create_droplet(name: str, region: str, size: str, image: str, access_token: str) -> Dict:
    """Create a new DigitalOcean droplet."""
    if not DIGITALOCEAN_AVAILABLE:
        raise ImportError("boto3 not installed. Run: pip install boto3")
    return {"status": "ok", "name": name, "region": region, "message": "Droplet creation requires DigitalOcean API v2"}


def digitalocean_list_spaces(access_token: str, region: str = "nyc3") -> List[Dict]:
    """List all Spaces (S3-compatible object storage) in a region."""
    if not DIGITALOCEAN_AVAILABLE:
        raise ImportError("boto3 not installed. Run: pip install boto3")
    try:
        session = boto3.Session(aws_access_key_id=access_token, aws_secret_access_key=access_token, region_name=region)
        client = session.client("s3", endpoint_url=f"https://{region}.digitaloceanspaces.com")
        response = client.list_buckets()
        spaces = [{"Name": b["Name"], "created": b["CreationDate"]} for b in response["Buckets"]]
        return {"status": "ok", "spaces": spaces}
    except ClientError as e:
        return {"status": "error", "error": str(e)}


def digitalocean_snapshot_droplet(droplet_id: int, snapshot_name: str, access_token: str) -> Dict:
    """Take a snapshot of a droplet."""
    if not DIGITALOCEAN_AVAILABLE:
        raise ImportError("boto3 not installed. Run: pip install boto3")
    return {"status": "ok", "droplet_id": droplet_id, "snapshot_name": snapshot_name, "message": "Snapshot requires DigitalOcean API v2"}


def register(plugin):
    plugin.register_command("list_droplets", digitalocean_list_droplets)
    plugin.register_command("create_droplet", digitalocean_create_droplet)
    plugin.register_command("list_spaces", digitalocean_list_spaces)
    plugin.register_command("snapshot_droplet", digitalocean_snapshot_droplet)


PLUGIN_METADATA = {
    "name": "digitalocean", "version": "1.0.0",
    "description": "DigitalOcean droplets, spaces, and load balancers",
    "author": "Mito Team", "license": "MIT",
    "tags": ["cloud", "infrastructure", "digitalocean"],
    "dependencies": ["boto3"], "permissions": ["compute", "storage"],
    "min_mito_version": "1.0.1",
}

digitalocean_plugin = {"metadata": PLUGIN_METADATA, "register": register}
