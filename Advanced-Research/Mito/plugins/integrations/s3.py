"""
AWS S3 Integration Plugin
Upload, download, list, delete files from S3
"""

import os
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger("mito.plugins.s3")


class S3Client:
    def __init__(self, bucket: Optional[str] = None, region: Optional[str] = None,
                 access_key: Optional[str] = None, secret_key: Optional[str] = None):
        self.bucket = bucket or os.environ.get("S3_BUCKET", "")
        self.region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self.access_key = access_key or os.environ.get("AWS_ACCESS_KEY_ID", "")
        self.secret_key = secret_key or os.environ.get("AWS_SECRET_ACCESS_KEY", "")
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import boto3
                self._client = boto3.client(
                    "s3",
                    region_name=self.region,
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                )
            except ImportError:
                raise ImportError("boto3 not installed. Install with: pip install boto3")
        return self._client

    def upload(self, local_path: str, s3_key: str, bucket: str = None,
               extra_args: Dict = None) -> Dict:
        client = self._get_client()
        target_bucket = bucket or self.bucket
        client.upload_file(local_path, target_bucket, s3_key, ExtraArgs=extra_args or {})
        logger.info(f"Uploaded {local_path} to s3://{target_bucket}/{s3_key}")
        return {"bucket": target_bucket, "key": s3_key, "size": os.path.getsize(local_path)}

    def upload_bytes(self, data: bytes, s3_key: str, bucket: str = None,
                     content_type: str = "application/octet-stream") -> Dict:
        client = self._get_client()
        target_bucket = bucket or self.bucket
        client.put_object(Bucket=target_bucket, Key=s3_key, Body=data, ContentType=content_type)
        logger.info(f"Uploaded {len(data)} bytes to s3://{target_bucket}/{s3_key}")
        return {"bucket": target_bucket, "key": s3_key, "size": len(data)}

    def download(self, s3_key: str, local_path: str, bucket: str = None) -> Dict:
        client = self._get_client()
        target_bucket = bucket or self.bucket
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        client.download_file(target_bucket, s3_key, local_path)
        logger.info(f"Downloaded s3://{target_bucket}/{s3_key} to {local_path}")
        return {"key": s3_key, "local_path": local_path}

    def download_bytes(self, s3_key: str, bucket: str = None) -> bytes:
        client = self._get_client()
        target_bucket = bucket or self.bucket
        resp = client.get_object(Bucket=target_bucket, Key=s3_key)
        return resp["Body"].read()

    def list_objects(self, prefix: str = "", bucket: str = None,
                     max_keys: int = 1000) -> List[Dict]:
        client = self._get_client()
        target_bucket = bucket or self.bucket
        resp = client.list_objects_v2(Bucket=target_bucket, Prefix=prefix, MaxKeys=max_keys)
        return [{"key": obj["Key"], "size": obj["Size"], "last_modified": str(obj["LastModified"])}
                for obj in resp.get("Contents", [])]

    def delete(self, s3_key: str, bucket: str = None) -> bool:
        client = self._get_client()
        target_bucket = bucket or self.bucket
        client.delete_object(Bucket=target_bucket, Key=s3_key)
        logger.info(f"Deleted s3://{target_bucket}/{s3_key}")
        return True

    def generate_presigned_url(self, s3_key: str, bucket: str = None,
                               expires_in: int = 3600) -> str:
        client = self._get_client()
        target_bucket = bucket or self.bucket
        return client.generate_presigned_url(
            "get_object",
            Params={"Bucket": target_bucket, "Key": s3_key},
            ExpiresIn=expires_in,
        )

    def object_exists(self, s3_key: str, bucket: str = None) -> bool:
        client = self._get_client()
        target_bucket = bucket or self.bucket
        try:
            client.head_object(Bucket=target_bucket, Key=s3_key)
            return True
        except Exception:
            return False

    def copy(self, source_key: str, dest_key: str, source_bucket: str = None,
             dest_bucket: str = None) -> Dict:
        client = self._get_client()
        src_bkt = source_bucket or self.bucket
        dst_bkt = dest_bucket or self.bucket
        client.copy_object(
            Bucket=dst_bkt,
            Key=dest_key,
            CopySource={"Bucket": src_bkt, "Key": source_key},
        )
        return {"source": f"s3://{src_bkt}/{source_key}", "dest": f"s3://{dst_bkt}/{dest_key}"}


def s3_upload_cmd(local_path: str = "", s3_key: str = "") -> Dict:
    """Upload a file to S3."""
    client = S3Client()
    return client.upload(local_path, s3_key)


def s3_download_cmd(s3_key: str = "", local_path: str = "") -> Dict:
    """Download a file from S3."""
    client = S3Client()
    return client.download(s3_key, local_path)


def s3_list_cmd(prefix: str = "") -> List[Dict]:
    """List objects in S3 bucket."""
    client = S3Client()
    return client.list_objects(prefix=prefix)


def s3_delete_cmd(s3_key: str = "") -> bool:
    """Delete an object from S3."""
    client = S3Client()
    return client.delete(s3_key)


def register(plugin):
    plugin.register_command("s3_upload", s3_upload_cmd)
    plugin.register_command("s3_download", s3_download_cmd)
    plugin.register_command("s3_list", s3_list_cmd)
    plugin.register_command("s3_delete", s3_delete_cmd)
    plugin.set_resource("client_class", S3Client)


PLUGIN_METADATA = {
    "name": "s3",
    "version": "1.0.0",
    "description": "AWS S3 integration - Upload, download, list, delete files",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["aws", "s3", "storage", "files"],
    "dependencies": ["boto3"],
    "permissions": ["network_access", "read_env", "read_files", "write_files"],
    "min_mito_version": "1.0.0",
}


s3_plugin = {
    "metadata": PLUGIN_METADATA,
    "register": register,
}
