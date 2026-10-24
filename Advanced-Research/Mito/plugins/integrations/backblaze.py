"""
Backblaze B2 Plugin
Cloud backup and S3-compatible object storage.
"""
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.backblaze")

try:
    from b2sdk.v1 import InMemoryAccountInfo, B2Api
    B2_AVAILABLE = True
except ImportError:
    B2_AVAILABLE = False


def _api(key_id: str = "", app_key: str = ""):
    import os
    if not B2_AVAILABLE:
        raise ImportError("b2sdk not installed. Run: pip install b2sdk")
    info = InMemoryAccountInfo()
    api = B2Api(info)
    api.authorize_account("production", key_id or os.environ.get("B2_KEY_ID", ""), app_key or os.environ.get("B2_APP_KEY", ""))
    return api


def backblaze_upload_file_cmd(bucket: str = "", file_path: str = "", file_name: str = "") -> Dict:
    api = _api()
    bucket_obj = api.get_bucket_by_name(bucket)
    file_obj = bucket_obj.upload_local_file(file_path, file_name or file_path.split("/")[-1])
    return {"file_id": file_obj.id_, "file_name": file_obj.file_name, "bucket": bucket, "status": "uploaded"}


def backblaze_download_file_cmd(file_id: str = "", output_path: str = "") -> Dict:
    api = _api()
    api.download_file_by_id(file_id).save_to(output_path)
    return {"file_id": file_id, "output": output_path, "status": "downloaded"}


def backblaze_list_files_cmd(bucket: str = "", prefix: str = "", limit: int = 100) -> Dict:
    api = _api()
    bucket_obj = api.get_bucket_by_name(bucket)
    files = list(bucket_obj.list_file_versions(prefix=prefix, batch_size=limit))
    return {"files": [{"name": f.file_name, "id": f.id_, "size": f.size} for f in files], "count": len(files)}


def backblaze_delete_file_cmd(file_id: str = "", file_name: str = "") -> Dict:
    api = _api()
    api.delete_file_version(file_id, file_name)
    return {"file_id": file_id, "status": "deleted"}


def backblaze_create_bucket_cmd(name: str = "", bucket_type: str = "allPrivate") -> Dict:
    api = _api()
    bucket = api.create_bucket(name, bucket_type)
    return {"bucket": name, "type": bucket_type, "id": bucket.id_, "status": "created"}


def register(plugin):
    plugin.register_command("upload_file", backblaze_upload_file_cmd)
    plugin.register_command("download_file", backblaze_download_file_cmd)
    plugin.register_command("list_files", backblaze_list_files_cmd)
    plugin.register_command("delete_file", backblaze_delete_file_cmd)
    plugin.register_command("create_bucket", backblaze_create_bucket_cmd)


PLUGIN_METADATA = {
    "name": "backblaze", "version": "1.0.0",
    "description": "Backblaze B2 cloud backup and object storage",
    "author": "Mito Team", "license": "MIT",
    "tags": ["backblaze", "backup", "storage", "cloud"],
    "dependencies": ["b2sdk"], "permissions": ["backblaze_access"],
    "min_mito_version": "1.0.1",
}

backblaze_plugin = {"metadata": PLUGIN_METADATA, "register": register}
