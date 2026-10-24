"""
Shell Command Plugin
Execute shell commands with timeout, env vars, and capture.
"""

import os
import subprocess
import logging
import shlex
from typing import Dict, List, Optional

logger = logging.getLogger("mito.plugins.shell")


class ShellClient:
    def __init__(self, cwd: str = None, env: Dict = None, timeout: int = 30):
        self.cwd = cwd or os.getcwd()
        self.env = env or dict(os.environ)
        self.timeout = timeout
        self._deny_commands = {"rm -rf /", "dd if=", ":(){:|:&};:"}

    def _check_command(self, cmd: str):
        for deny in self._deny_commands:
            if deny in cmd:
                raise PermissionError(f"Dangerous command denied: {cmd}")

    def run(self, command: str, timeout: int = None, shell: bool = True) -> Dict:
        self._check_command(command)
        try:
            if shell:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=self.cwd,
                    env=self.env,
                    capture_output=True,
                    text=True,
                    timeout=timeout or self.timeout,
                )
            else:
                args = shlex.split(command)
                result = subprocess.run(
                    args,
                    cwd=self.cwd,
                    env=self.env,
                    capture_output=True,
                    text=True,
                    timeout=timeout or self.timeout,
                )
            return {
                "command": command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {
                "command": command,
                "error": f"Command timed out after {timeout or self.timeout}s",
                "returncode": -1,
                "success": False,
            }
        except Exception as e:
            return {
                "command": command,
                "error": str(e),
                "returncode": -1,
                "success": False,
            }

    def run_pipeline(self, commands: List[str]) -> List[Dict]:
        results = []
        for cmd in commands:
            results.append(self.run(cmd))
        return results

    def env_get(self, key: str) -> str:
        return self.env.get(key, os.environ.get(key, ""))

    def env_set(self, key: str, value: str) -> Dict:
        self.env[key] = value
        return {"key": key, "value": value, "set": True}

    def which(self, command: str) -> Optional[str]:
        result = self.run(f"which {shlex.quote(command)}", shell=True)
        return result["stdout"].strip() if result["success"] else None


def shell_run_cmd(command: str = "", timeout: int = 30, cwd: str = "") -> Dict:
    """Run a shell command and return stdout, stderr, and return code."""
    client = ShellClient(cwd=cwd or None, timeout=timeout)
    return client.run(command, timeout=timeout)


def shell_run_script_cmd(script: str = "", cwd: str = "") -> List[Dict]:
    """Run multiple commands as a pipeline."""
    client = ShellClient(cwd=cwd or None)
    return client.run_pipeline(script.split("&&"))


def shell_which_cmd(command: str = "") -> Optional[str]:
    """Find the full path of a command."""
    return ShellClient().which(command)


def register(plugin):
    plugin.register_command("shell_run", shell_run_cmd)
    plugin.register_command("shell_run_script", shell_run_script_cmd)
    plugin.register_command("shell_which", shell_which_cmd)
    plugin.set_resource("client_class", ShellClient)


PLUGIN_METADATA = {
    "name": "shell",
    "version": "1.0.0",
    "description": "Execute shell commands with timeout and env var support",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["shell", "bash", "command", "execute"],
    "dependencies": [],
    "permissions": ["execute_commands", "read_env"],
    "min_mito_version": "1.0.1",
}


shell_plugin = {"metadata": PLUGIN_METADATA, "register": register}
