import subprocess

from typing import List


def get_running_machines() -> List[str]:
    try:
        result = subprocess.run(
            ["VBoxManage", "list", "runningvms"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except:
        print("failed to get list of vms")
        return []

    try:
        running_vms: List[str] = []
        for line in result.stdout.splitlines():
            vm_name = line.split('"')[1]
            running_vms.append(vm_name)
    except:
        print("failed to parse subprocess output while trying to get list of vms")
        return []

    return running_vms

def start_machine(machine_name: str):
    try:
        subprocess.run(
            ["VBoxManage", "startvm", machine_name, "--type", "headless"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to start VM: {e.stderr}")
        return False

def stop_machine(machine_name: str):
    try:
        subprocess.run(
            ["VBoxManage", "controlvm", machine_name, "savestate"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop VM: {e.stderr}")
        return False