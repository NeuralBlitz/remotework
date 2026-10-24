"""
Wasabi Plugin
S3-compatible object storage via Wasabi.
"""
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.wasabi")

try:
    import boto3
    BOTO_AVAILABLE = True
except ImportError:
    BOTO_AVAILABLE = False


ENDPOINTS = {
    "us-east-1": "s3.wasabisys.com",
    "us-east-2": "s3.us-east-2.wasabisys.com",
    "us-west-1": "s3.us-west-1.wasabisys.com",
    "eu-central-1": "s3.eu-central-1.wasabisys.com",
    "ap-northeast-1": "s3.ap-northeast-1.wasabisys.com",
}


def _s3(region: str = "us-east-1", access_key: str = "", secret_key: str = ""):
    import os
    if not BOTO_AVAILABLE:
        raise ImportError("boto3 not installed. Run: pip install boto3")
    return boto3.client(
        "s3", region_name=region,
        aws_access_key_id=access_key or os.environ.get("WASABI_ACCESS_KEY", ""),
        aws_secret_access_key=secret_key or os.environ.get("WASABI_SECRET_KEY", ""),
        endpoint_url=f"https://{ENDPOINTS.get(region, ENDPOINTS['us-east-1'])}",
    )


def wasabi_list_buckets_cmd(region: str = "us-east-1") -> List[Dict]:
    s3 = _s3(region)
    buckets = s3.list_buckets().get("Buckets", [])
    return {"buckets": [{"name": b["Name"], "created": b["CreationDate"].isoformat()} for b in buckets], "count": len(buckets)}


def wasabi_upload_cmd(bucket: str = "", file_path: str = "", key: str = "", region: str = "us-east-1") -> Dict:
    s3 = _s3(region)
    s3.upload_file(file_path, bucket, key or file_path.split("/")[-1])
    return {"bucket": bucket, "key": key, "status": "uploaded"}


def wasabi_download_cmd(bucket: str = "", key: str = "", output: str = "", region: str = "us-east-1") -> Dict:
    s3 = _s3(region)
    s3.download_file(bucket, key, output or key.split("/")[-1])
    return {"bucket": bucket, "key": key, "output": output, "status": "downloaded"}


def wasabi_list_objects_cmd(bucket: str = "", prefix: str = "", region: str = "us-east-1") -> Dict:
    s3 = _s3(region)
    result = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    objects = result.get("Contents", [])
    return {"objects": [{"key": o["Key"], "size": o["Size"]} for o in objects], "count": len(objects)}


def wasabi_delete_bucket_cmd(bucket: str = "", region: str = "us-east-1") -> Dict:
    s3 = _s3(region)
    s3.delete_bucket(Bucket=bucket)
    return {"bucket": bucket, "status": "deleted"}


def register(plugin):
    plugin.register_command("list_buckets", wasabi_list_buckets_cmd)
    plugin.register_command("upload", wasabi_upload_cmd)
    plugin.register_command("download", wasabi_download_cmd)
    plugin.register_command("list_objects", wasabi_list_objects_cmd)
    plugin.register_command("delete_bucket", wasabi_delete_bucket_cmd)


PLUGIN_METADATA = {
    "name": "wasabi", "version": "1.0.0",
    "description": "Wasabi S3-compatible object storage",
    "author": "Mito Team", "license": "MIT",
    "tags": ["wasabi", "storage", "s3", "cloud"],
    "dependencies": ["boto3"], "permissions": ["wasabi_access"],
    "min_mito_version": "1.0.1",
}

wasabi_plugin = {"metadata": PLUGIN_METADATA, "register": register}
