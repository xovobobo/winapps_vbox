import subprocess

def get_active_rdp_connections(ip: str, port: int):
    try:
        result = subprocess.run(
            ["lsof", "-i", f"tcp@{ip}:{port}"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return max(0, len(result.stdout.splitlines()) - 1)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:  # No connections found
            return 0
        print(f"Error checking connections: {e.stderr}")
        return 0
    except FileNotFoundError:
        return 0
