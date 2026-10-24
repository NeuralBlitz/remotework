"""
Docker Plugin
Container lifecycle management via Docker Engine API.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.docker")

try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False


def _client():
    if not DOCKER_AVAILABLE:
        raise ImportError("docker not installed. Run: pip install docker")
    return docker.from_env()


def docker_list_containers_cmd(all: bool = False) -> List[Dict]:
    client = _client()
    containers = client.containers.list(all=all)
    return [{"id": c.id[:12], "name": c.name, "image": c.image.tags, "status": c.status, "ports": c.ports} for c in containers]


def docker_run_container_cmd(image: str = "", name: str = "", command: str = "", detach: bool = True) -> Dict:
    client = _client()
    container = client.containers.run(image, command=command or None, name=name or None, detach=detach, remove=True)
    return {"id": container.id[:12], "status": container.status, "name": name or container.short_id}


def docker_stop_container_cmd(container_id: str = "") -> Dict:
    client = _client()
    container = client.containers.get(container_id)
    container.stop(timeout=10)
    return {"id": container_id, "status": "stopped"}


def docker_pull_image_cmd(image: str = "", tag: str = "latest") -> Dict:
    client = _client()
    for line in client.api.pull(image, tag=tag, stream=True, decode=True):
        pass
    return {"image": f"{image}:{tag}", "status": "pulled"}


def docker_list_images_cmd() -> List[Dict]:
    client = _client()
    images = client.images.list()
    return [{"id": i.id.replace("sha256:", "")[:12], "tags": i.tags, "size": i.attrs.get("Size", 0)} for i in images]


def docker_logs_cmd(container_id: str = "", tail: int = 100) -> str:
    client = _client()
    container = client.containers.get(container_id)
    logs = container.logs(tail=tail, timestamps=True).decode()
    return {"container": container_id, "logs": logs, "lines": len(logs.splitlines())}


def docker_remove_container_cmd(container_id: str = "", force: bool = False) -> Dict:
    client = _client()
    container = client.containers.get(container_id)
    container.remove(force=force)
    return {"id": container_id, "status": "removed"}


def register(plugin):
    plugin.register_command("list_containers", docker_list_containers_cmd)
    plugin.register_command("run_container", docker_run_container_cmd)
    plugin.register_command("stop_container", docker_stop_container_cmd)
    plugin.register_command("pull_image", docker_pull_image_cmd)
    plugin.register_command("list_images", docker_list_images_cmd)
    plugin.register_command("logs", docker_logs_cmd)
    plugin.register_command("remove_container", docker_remove_container_cmd)


PLUGIN_METADATA = {
    "name": "docker", "version": "1.0.0",
    "description": "Docker container lifecycle management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["docker", "containers", "devops"],
    "dependencies": ["docker"], "permissions": ["docker_access"],
    "min_mito_version": "1.0.1",
}

docker_plugin = {"metadata": PLUGIN_METADATA, "register": register}
