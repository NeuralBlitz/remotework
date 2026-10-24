"""
Ansible Plugin
Run playbooks, ping hosts, and execute modules via Ansible.
"""
import subprocess
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.ansible")


def ansible_run_playbook_cmd(playbook: str = "", inventory: str = "", extra_vars: str = "") -> Dict:
    args = ["ansible-playbook", playbook]
    if inventory:
        args.extend(["-i", inventory])
    if extra_vars:
        args.extend(["-e", extra_vars])
    result = subprocess.run(args, capture_output=True, text=True, timeout=600)
    return {"returncode": result.returncode, "stdout": result.stdout[-3000:], "stderr": result.stderr[-1000:]}


def ansible_ping_cmd(host: str = "", inventory: str = "") -> Dict:
    args = ["ansible", host, "-i", inventory or "localhost,", "-m", "ping"]
    result = subprocess.run(args, capture_output=True, text=True, timeout=30)
    return {"returncode": result.returncode, "output": result.stdout + result.stderr}


def ansible_list_hosts_cmd(inventory: str = "") -> Dict:
    args = ["ansible-inventory", "-i", inventory or "localhost,"]
    if not inventory:
        args = ["ansible-inventory", "--list"]
    result = subprocess.run(args, capture_output=True, text=True, timeout=30)
    import json
    try:
        return {"inventory": json.loads(result.stdout)}
    except Exception:
        return {"raw": result.stdout}


def ansible_run_module_cmd(host: str = "", module: str = "", args: str = "", inventory: str = "") -> Dict:
    cmd = ["ansible", host, "-i", inventory or "localhost,", "-m", module, "-a", args or '""']
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    return {"returncode": result.returncode, "output": result.stdout + result.stderr}


def ansible_facts_cmd(host: str = "", inventory: str = "") -> Dict:
    args = ["ansible", host, "-i", inventory or "localhost,", "-m", "setup"]
    result = subprocess.run(args, capture_output=True, text=True, timeout=60)
    return {"facts": result.stdout[-3000:]}


def ansible_galaxy_install_cmd(role: str = "", galaxy_server: str = "") -> Dict:
    args = ["ansible-galaxy", "role", "install", role]
    if galaxy_server:
        args.extend(["--server", galaxy_server])
    result = subprocess.run(args, capture_output=True, text=True, timeout=120)
    return {"returncode": result.returncode, "stdout": result.stdout[-1000:]}


def register(plugin):
    plugin.register_command("run_playbook", ansible_run_playbook_cmd)
    plugin.register_command("ping_host", ansible_ping_cmd)
    plugin.register_command("list_hosts", ansible_list_hosts_cmd)
    plugin.register_command("run_module", ansible_run_module_cmd)
    plugin.register_command("facts", ansible_facts_cmd)
    plugin.register_command("galaxy_install", ansible_galaxy_install_cmd)


PLUGIN_METADATA = {
    "name": "ansible", "version": "1.0.0",
    "description": "Ansible playbook execution and host management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["ansible", "automation", "devops", "config"],
    "dependencies": ["ansible"], "permissions": ["shell_access"],
    "min_mito_version": "1.0.1",
}

ansible_plugin = {"metadata": PLUGIN_METADATA, "register": register}
