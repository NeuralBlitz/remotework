"""
Kubernetes Plugin
Pod, deployment, and cluster management via Kubernetes API.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.kubernetes")

try:
    from kubernetes import client, config
    K8S_AVAILABLE = True
except ImportError:
    K8S_AVAILABLE = False


def _core():
    if not K8S_AVAILABLE:
        raise ImportError("kubernetes not installed. Run: pip install kubernetes")
    try:
        config.load_kube_config()
    except Exception:
        config.load_incluster_config()
    return client.CoreV1Api()


def kubernetes_list_pods_cmd(namespace: str = "default", label: str = "") -> List[Dict]:
    api = _core()
    if label:
        filtered = api.list_namespaced_pod(namespace, label_selector=label)
        pods = filtered.items
    else:
        pods = api.list_namespaced_pod(namespace).items
    return [{"name": p.metadata.name, "phase": p.status.phase, "ip": p.status.pod_ip, "node": p.spec.node_name} for p in pods]


def kubernetes_get_pod_cmd(name: str = "", namespace: str = "default") -> Dict:
    api = _core()
    p = api.read_namespaced_pod(name, namespace)
    return {"name": p.metadata.name, "namespace": p.metadata.namespace, "phase": p.status.phase, "containers": [c.name for c in p.spec.containers]}


def kubernetes_create_deployment_cmd(name: str = "", image: str = "", replicas: int = 1, namespace: str = "default") -> Dict:
    if not K8S_AVAILABLE:
        raise ImportError("kubernetes not installed")
    from kubernetes import client
    api = client.AppsV1Api()
    body = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(match_labels={"app": name}),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": name}),
                spec=client.V1PodSpec(containers=[client.V1Container(name=name, image=image)])
            )
        )
    )
    api.create_namespaced_deployment(namespace=namespace, body=body)
    return {"name": name, "replicas": replicas, "image": image, "status": "created"}


def kubernetes_scale_deployment_cmd(name: str = "", replicas: int = 1, namespace: str = "default") -> Dict:
    if not K8S_AVAILABLE:
        raise ImportError("kubernetes not installed")
    from kubernetes import client
    api = client.AppsV1Api()
    body = {"spec": {"replicas": replicas}}
    api.patch_namespaced_deployment_scale(name, namespace, body)
    return {"name": name, "replicas": replicas, "status": "scaled"}


def kubernetes_get_logs_cmd(name: str = "", namespace: str = "default", tail: int = 100) -> str:
    api = _core()
    logs = api.read_namespaced_pod_log(name, namespace, tail_lines=tail)
    return {"pod": name, "logs": logs}


def kubernetes_delete_pod_cmd(name: str = "", namespace: str = "default") -> Dict:
    api = _core()
    api.delete_namespaced_pod(name, namespace)
    return {"name": name, "status": "deleted"}


def register(plugin):
    plugin.register_command("list_pods", kubernetes_list_pods_cmd)
    plugin.register_command("get_pod", kubernetes_get_pod_cmd)
    plugin.register_command("create_deployment", kubernetes_create_deployment_cmd)
    plugin.register_command("scale_deployment", kubernetes_scale_deployment_cmd)
    plugin.register_command("get_logs", kubernetes_get_logs_cmd)
    plugin.register_command("delete_pod", kubernetes_delete_pod_cmd)


PLUGIN_METADATA = {
    "name": "kubernetes", "version": "1.0.0",
    "description": "Kubernetes pod, deployment, and cluster management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["kubernetes", "k8s", "containers", "devops"],
    "dependencies": ["kubernetes"], "permissions": ["k8s_access"],
    "min_mito_version": "1.0.1",
}

kubernetes_plugin = {"metadata": PLUGIN_METADATA, "register": register}
