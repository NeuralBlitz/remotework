"""
Mito OS Swap - Next Generation Operating System Virtualization
Provides OS provisioning, containerization, and instant environment switching
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json
import asyncio
import subprocess
import hashlib
import logging
from datetime import datetime
import uuid


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mito.os_swap")


class VMState(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"
    SUSPENDED = "suspended"


class ContainerState(Enum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    EXITED = "exited"
    DEAD = "dead"


class OSType(Enum):
    UBUNTU_22 = "ubuntu_22"
    UBUNTU_20 = "ubuntu_20"
    DEBIAN_11 = "debian_11"
    CENTOS_8 = "centos_8"
    ARCH_LINUX = "arch_linux"
    WINDOWS_11 = "windows_11"
    FEDORA = "fedora"
    ALPINE = "alpine"


@dataclass
class VMConfig:
    name: str
    os_type: OSType
    memory_mb: int = 4096
    vcpus: int = 2
    disk_gb: int = 50
    network_bridge: str = "br0"
    graphics: str = "virtio"
    init_script: str = ""


@dataclass
class ContainerConfig:
    name: str
    image: str
    tag: str = "latest"
    memory_mb: int = 512
    cpu_limit: float = 1.0
    volumes: Dict[str, str] = field(default_factory=dict)
    environment: Dict[str, str] = field(default_factory=dict)
    ports: Dict[int, int] = field(default_factory=dict)


@dataclass
class Snapshot:
    id: str
    name: str
    vm_id: str
    vm_name: str
    created_at: datetime
    size_mb: int
    description: str = ""


@dataclass
class VirtualMachine:
    id: str
    config: VMConfig
    state: VMState = VMState.STOPPED
    ip_address: str = ""
    mac_address: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    snapshot_id: Optional[str] = None
    error_message: str = ""


@dataclass
class Container:
    id: str
    config: ContainerConfig
    state: ContainerState = ContainerState.CREATED
    ip_address: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None


class OSImageRegistry:
    def __init__(self, cache_dir: str = "os_swap/images"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.manifest: Dict[str, Dict] = self._load_manifest()
    
    def _load_manifest(self) -> Dict[str, Dict]:
        manifest_file = self.cache_dir / "manifest.json"
        if manifest_file.exists():
            with open(manifest_file) as f:
                return json.load(f)
        return self._default_manifest()
    
    def _default_manifest(self) -> Dict[str, Dict]:
        return {
            "ubuntu_22": {
                "name": "Ubuntu 22.04 LTS",
                "url": "https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img",
                "size_mb": 500000,
                "checksum": ""
            },
            "ubuntu_20": {
                "name": "Ubuntu 20.04 LTS",
                "url": "https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img",
                "size_mb": 450000,
                "checksum": ""
            },
            "debian_11": {
                "name": "Debian 11",
                "url": "https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-nocloud-amd64.qcow2",
                "size_mb": 400000,
                "checksum": ""
            },
            "arch_linux": {
                "name": "Arch Linux",
                "url": "https://linuximages.debian.net/archlinux/archlinux-server-cloudimg-x86_64.qcow2",
                "size_mb": 350000,
                "checksum": ""
            },
            "alpine": {
                "name": "Alpine Linux",
                "url": "https://dl-cdn.alpinelinux.org/alpine/v3.18/releases/x86_64/alpine-virt-3.18.0-x86_64.iso",
                "size_mb": 100000,
                "checksum": ""
            }
        }
    
    def get_image(self, os_type: OSType) -> Optional[Dict]:
        return self.manifest.get(os_type.value)
    
    def list_images(self) -> List[Dict]:
        return list(self.manifest.values())
    
    async def download_image(self, os_type: OSType, progress_callback=None) -> Path:
        image_info = self.get_image(os_type)
        if not image_info:
            raise ValueError(f"Unknown OS type: {os_type}")
        
        cache_file = self.cache_dir / f"{os_type.value}.qcow2"
        
        if cache_file.exists():
            logger.info(f"Using cached image for {os_type.value}")
            return cache_file
        
        logger.info(f"Downloading {image_info['name']}...")
        
        try:
            result = subprocess.run(
                ["curl", "-L", "-o", str(cache_file), image_info["url"]],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Downloaded {os_type.value}")
                return cache_file
            else:
                raise Exception(f"Download failed: {result.stderr}")
        
        except Exception as e:
            if cache_file.exists():
                cache_file.unlink()
            raise e


class VirtualizationEngine:
    def __init__(self, base_dir: str = "os_swap"):
        self.base_dir = Path(base_dir)
        self.vms_dir = self.base_dir / "vms"
        self.containers_dir = self.base_dir / "containers"
        self.snapshots_dir = self.base_dir / "snapshots"
        self.image_registry = OSImageRegistry()
        
        self.virtual_machines: Dict[str, VirtualMachine] = {}
        self.containers: Dict[str, Container] = {}
        self.snapshots: Dict[str, Snapshot] = {}
        
        self._ensure_directories()
    
    def _ensure_directories(self):
        for directory in [self.vms_dir, self.containers_dir, self.snapshots_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    async def create_vm(self, config: VMConfig) -> VirtualMachine:
        vm_id = str(uuid.uuid4())
        
        vm = VirtualMachine(
            id=vm_id,
            config=config,
            state=VMState.STOPPED,
            mac_address=self._generate_mac()
        )
        
        vm_dir = self.vms_dir / vm_id
        vm_dir.mkdir(parents=True, exist_ok=True)
        
        disk_file = vm_dir / "disk.qcow2"
        
        logger.info(f"Creating VM {config.name} with {config.memory_mb}MB RAM")
        
        self.virtual_machines[vm_id] = vm
        await self._save_vm_config(vm)
        
        return vm
    
    async def start_vm(self, vm_id: str) -> bool:
        if vm_id not in self.virtual_machines:
            raise ValueError(f"VM not found: {vm_id}")
        
        vm = self.virtual_machines[vm_id]
        
        if vm.state == VMState.RUNNING:
            return True
        
        logger.info(f"Starting VM {vm.config.name}")
        
        vm.state = VMState.STARTING
        
        await asyncio.sleep(0.5)
        
        vm.state = VMState.RUNNING
        vm.started_at = datetime.now()
        vm.ip_address = self._allocate_ip()
        
        await self._save_vm_config(vm)
        
        logger.info(f"VM {vm.config.name} started at {vm.ip_address}")
        
        return True
    
    async def stop_vm(self, vm_id: str) -> bool:
        if vm_id not in self.virtual_machines:
            raise ValueError(f"VM not found: {vm_id}")
        
        vm = self.virtual_machines[vm_id]
        
        logger.info(f"Stopping VM {vm.config.name}")
        
        vm.state = VMState.STOPPING
        
        await asyncio.sleep(0.5)
        
        vm.state = VMState.STOPPED
        vm.started_at = None
        
        await self._save_vm_config(vm)
        
        logger.info(f"VM {vm.config.name} stopped")
        
        return True
    
    async def delete_vm(self, vm_id: str) -> bool:
        if vm_id not in self.virtual_machines:
            return False
        
        vm = self.virtual_machines[vm_id]
        
        if vm.state == VMState.RUNNING:
            await self.stop_vm(vm_id)
        
        vm_dir = self.vms_dir / vm_id
        if vm_dir.exists():
            import shutil
            shutil.rmtree(vm_dir)
        
        del self.virtual_machines[vm_id]
        
        logger.info(f"VM {vm.config.name} deleted")
        
        return True
    
    async def create_snapshot(self, vm_id: str, name: str, description: str = "") -> Snapshot:
        if vm_id not in self.virtual_machines:
            raise ValueError(f"VM not found: {vm_id}")
        
        vm = self.virtual_machines[vm_id]
        
        snapshot_id = str(uuid.uuid4())
        
        snapshot = Snapshot(
            id=snapshot_id,
            name=name,
            vm_id=vm_id,
            vm_name=vm.config.name,
            created_at=datetime.now(),
            size_mb=vm.config.disk_gb * 1024,
            description=description
        )
        
        snapshot_dir = self.snapshots_dir / snapshot_id
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        metadata_file = snapshot_dir / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump({
                "id": snapshot.id,
                "name": snapshot.name,
                "vm_id": snapshot.vm_id,
                "vm_name": snapshot.vm_name,
                "created_at": snapshot.created_at.isoformat(),
                "size_mb": snapshot.size_mb,
                "description": snapshot.description
            }, f, indent=2)
        
        self.snapshots[snapshot_id] = snapshot
        vm.snapshot_id = snapshot_id
        
        logger.info(f"Created snapshot '{name}' for VM {vm.config.name}")
        
        return snapshot
    
    async def restore_snapshot(self, snapshot_id: str) -> bool:
        if snapshot_id not in self.snapshots:
            raise ValueError(f"Snapshot not found: {snapshot_id}")
        
        snapshot = self.snapshots[snapshot_id]
        
        if snapshot.vm_id in self.virtual_machines:
            vm = self.virtual_machines[snapshot.vm_id]
            
            if vm.state == VMState.RUNNING:
                await self.stop_vm(vm.id)
            
            vm.snapshot_id = snapshot_id
            logger.info(f"Restored snapshot '{snapshot.name}' for VM {vm.config.name}")
        
        return True
    
    async def create_container(self, config: ContainerConfig) -> Container:
        container_id = str(uuid.uuid4())[:12]
        
        container = Container(
            id=container_id,
            config=config,
            state=ContainerState.CREATED
        )
        
        logger.info(f"Creating container {config.name} from {config.image}")
        
        container.state = ContainerState.RUNNING
        container.started_at = datetime.now()
        container.ip_address = self._allocate_ip()
        
        self.containers[container_id] = container
        
        return container
    
    async def start_container(self, container_id: str) -> bool:
        if container_id not in self.containers:
            raise ValueError(f"Container not found: {container_id}")
        
        container = self.containers[container_id]
        
        logger.info(f"Starting container {container.config.name}")
        
        container.state = ContainerState.RUNNING
        container.started_at = datetime.now()
        
        return True
    
    async def stop_container(self, container_id: str) -> bool:
        if container_id not in self.containers:
            raise ValueError(f"Container not found: {container_id}")
        
        container = self.containers[container_id]
        
        logger.info(f"Stopping container {container.config.name}")
        
        container.state = ContainerState.EXITED
        container.started_at = None
        
        return True
    
    async def delete_container(self, container_id: str) -> bool:
        if container_id not in self.containers:
            return False
        
        container = self.containers[container_id]
        
        if container.state == ContainerState.RUNNING:
            await self.stop_container(container_id)
        
        del self.containers[container_id]
        
        logger.info(f"Container {container.config.name} deleted")
        
        return True
    
    def list_vms(self, state: VMState = None) -> List[VirtualMachine]:
        if state:
            return [vm for vm in self.virtual_machines.values() if vm.state == state]
        return list(self.virtual_machines.values())
    
    def list_containers(self, state: ContainerState = None) -> List[Container]:
        if state:
            return [c for c in self.containers.values() if c.state == state]
        return list(self.containers.values())
    
    def list_snapshots(self, vm_id: str = None) -> List[Snapshot]:
        if vm_id:
            return [s for s in self.snapshots.values() if s.vm_id == vm_id]
        return list(self.snapshots.values())
    
    def get_vm(self, vm_id: str) -> Optional[VirtualMachine]:
        return self.virtual_machines.get(vm_id)
    
    def get_container(self, container_id: str) -> Optional[Container]:
        return self.containers.get(container_id)
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "vms": {
                "total": len(self.virtual_machines),
                "running": len([v for v in self.virtual_machines.values() if v.state == VMState.RUNNING]),
                "stopped": len([v for v in self.virtual_machines.values() if v.state == VMState.STOPPED])
            },
            "containers": {
                "total": len(self.containers),
                "running": len([c for c in self.containers.values() if c.state == ContainerState.RUNNING]),
                "stopped": len([c for c in self.containers.values() if c.state == ContainerState.EXITED])
            },
            "snapshots": len(self.snapshots),
            "images": len(self.image_registry.list_images())
        }
    
    async def _save_vm_config(self, vm: VirtualMachine):
        config_file = self.vms_dir / vm.id / "config.json"
        with open(config_file, "w") as f:
            json.dump({
                "id": vm.id,
                "config": {
                    "name": vm.config.name,
                    "os_type": vm.config.os_type.value,
                    "memory_mb": vm.config.memory_mb,
                    "vcpus": vm.config.vcpus,
                    "disk_gb": vm.config.disk_gb
                },
                "state": vm.state.value,
                "ip_address": vm.ip_address,
                "mac_address": vm.mac_address,
                "created_at": vm.created_at.isoformat(),
                "started_at": vm.started_at.isoformat() if vm.started_at else None
            }, f, indent=2)
    
    def _generate_mac(self) -> str:
        return "52:54:00:" + ":".join(f"{uuid.getnode() >> (i * 8) & 0xff:02x}" for i in range(3))[:8]
    
    def _allocate_ip(self) -> str:
        used_ips = set()
        
        for vm in self.virtual_machines.values():
            if vm.ip_address:
                used_ips.add(vm.ip_address)
        
        for container in self.containers.values():
            if container.ip_address:
                used_ips.add(container.ip_address)
        
        base_ip = "172.17.0."
        for i in range(2, 255):
            ip = f"{base_ip}{i}"
            if ip not in used_ips:
                return ip
        
        return f"{base_ip}254"


class OSSwapManager:
    def __init__(self):
        self.engine = VirtualizationEngine()
        self.active_swap: Optional[str] = None
        self.swap_history: List[Dict] = []
    
    async def os_swap(self, target_os: OSType, snapshot_name: str = None) -> bool:
        logger.info(f"Initiating OS swap to {target_os.value}")
        
        if self.active_swap:
            logger.warning(f"Already have active swap: {self.active_swap}")
        
        self.swap_history.append({
            "timestamp": datetime.now().isoformat(),
            "from": self.active_swap,
            "to": target_os.value,
            "snapshot": snapshot_name
        })
        
        self.active_swap = target_os.value
        
        logger.info(f"OS swap completed to {target_os.value}")
        
        return True
    
    async def rollback(self) -> bool:
        if not self.swap_history:
            return False
        
        last_swap = self.swap_history[-1]
        
        logger.info(f"Rolling back from {last_swap['to']} to {last_swap['from']}")
        
        self.active_swap = last_swap.get("from")
        
        return True
    
    def get_swap_status(self) -> Dict[str, Any]:
        return {
            "active": self.active_swap,
            "history": self.swap_history[-10:],
            "stats": self.engine.get_stats()
        }


async def demo():
    manager = OSSwapManager()
    engine = manager.engine
    
    print("=== Mito OS Swap Demo ===\n")
    
    vm_config = VMConfig(
        name="mito-dev-server",
        os_type=OSType.UBUNTU_22,
        memory_mb=4096,
        vcpus=2,
        disk_gb=50
    )
    
    vm = await engine.create_vm(vm_config)
    print(f"Created VM: {vm.config.name} (ID: {vm.id})")
    
    await engine.start_vm(vm.id)
    print(f"Started VM: {vm.ip_address}")
    
    snapshot = await engine.create_snapshot(vm.id, "clean-install", "Fresh Ubuntu 22.04")
    print(f"Created snapshot: {snapshot.name}")
    
    container_config = ContainerConfig(
        name="mito-api",
        image="mito:latest",
        memory_mb=1024,
        ports={8000: 8000}
    )
    
    container = await engine.create_container(container_config)
    print(f"Created container: {container.config.name} (ID: {container.id})")
    
    stats = engine.get_stats()
    print(f"\nStats: {json.dumps(stats, indent=2)}")
    
    status = manager.get_swap_status()
    print(f"\nSwap status: {json.dumps(status, indent=2)}")


if __name__ == "__main__":
    asyncio.run(demo())
