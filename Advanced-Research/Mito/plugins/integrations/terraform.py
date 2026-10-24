"""
Terraform Plugin
Infrastructure provisioning with Terraform CLI.
"""
import subprocess
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.terraform")


def terraform_init_cmd(workdir: str = ".", backend_config: str = "") -> Dict:
    args = ["terraform", "-chdir=" + workdir, "init"]
    if backend_config:
        args.extend(["-backend-config", backend_config])
    result = subprocess.run(args, capture_output=True, text=True, timeout=300)
    return {"returncode": result.returncode, "stdout": result.stdout[-2000:], "stderr": result.stderr[-1000:]}


def terraform_plan_cmd(workdir: str = ".", out_file: str = "") -> Dict:
    args = ["terraform", "-chdir=" + workdir, "plan"]
    if out_file:
        args.extend(["-out", out_file])
    result = subprocess.run(args, capture_output=True, text=True, timeout=600)
    return {"returncode": result.returncode, "stdout": result.stdout[-3000:], "changes": "plan created" if result.returncode == 0 else "plan failed"}


def terraform_apply_cmd(workdir: str = ".", auto_approve: bool = True) -> Dict:
    args = ["terraform", "-chdir=" + workdir, "apply"]
    if auto_approve:
        args.append("-auto-approve")
    result = subprocess.run(args, capture_output=True, text=True, timeout=600)
    return {"returncode": result.returncode, "stdout": result.stdout[-3000:], "stderr": result.stderr[-1000:]}


def terraform_destroy_cmd(workdir: str = ".", auto_approve: bool = True) -> Dict:
    args = ["terraform", "-chdir=" + workdir, "destroy"]
    if auto_approve:
        args.append("-auto-approve")
    result = subprocess.run(args, capture_output=True, text=True, timeout=600)
    return {"returncode": result.returncode, "stdout": result.stdout[-3000:]}


def terraform_validate_cmd(workdir: str = ".") -> Dict:
    result = subprocess.run(["terraform", "-chdir=" + workdir, "validate"], capture_output=True, text=True, timeout=60)
    return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def terraform_show_cmd(workdir: str = ".", state_file: str = "") -> str:
    args = ["terraform", "-chdir=" + workdir, "show"]
    if state_file:
        args.append(state_file)
    result = subprocess.run(args, capture_output=True, text=True, timeout=60)
    return {"output": result.stdout[-5000:]}


def terraform_output_cmd(workdir: str = ".") -> Dict:
    result = subprocess.run(["terraform", "-chdir=" + workdir, "output", "-json"], capture_output=True, text=True, timeout=30)
    import json
    try:
        return {"outputs": json.loads(result.stdout)}
    except Exception:
        return {"raw": result.stdout}


def register(plugin):
    plugin.register_command("init", terraform_init_cmd)
    plugin.register_command("plan", terraform_plan_cmd)
    plugin.register_command("apply", terraform_apply_cmd)
    plugin.register_command("destroy", terraform_destroy_cmd)
    plugin.register_command("validate", terraform_validate_cmd)
    plugin.register_command("show", terraform_show_cmd)
    plugin.register_command("output", terraform_output_cmd)


PLUGIN_METADATA = {
    "name": "terraform", "version": "1.0.0",
    "description": "Terraform infrastructure as code provisioning",
    "author": "Mito Team", "license": "MIT",
    "tags": ["terraform", "infrastructure", "iac", "devops"],
    "dependencies": ["terraform"], "permissions": ["shell_access"],
    "min_mito_version": "1.0.1",
}

terraform_plugin = {"metadata": PLUGIN_METADATA, "register": register}
