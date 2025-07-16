# Installation

```
pip install git+https://github.com/xovobobo/winapps_vbox.git
```

# Usage

## MIME

- By default there are 2 MIME associations added:
    - [Excel](winapps_vbox/apps/excel/ms-excel-winapps.desktop)
    - [Word](winapps_vbox/apps/word/ms-word-winapps.desktop)

Right-click an file (e.g. `.xlsx` or `.docx`) "Open With"

## CLI

- Start RDP session

    ```
    winapps_launch
    ```

- Start RDP app

    ```
    winapps_launch WINWORD.exe test.docx
    ```



# Configure VBox

1. Install a Windows VM using Oracle VirtualBox. (default VM name is `win10`)
2. Add a new user (default is `rdp`) to the Windows VM (`compmmgmt.msc`). Add password (default is `rdp123`)
    - If the current user has no password, set one - otherwise Windows automatically logs in on startup, which prevents new RDP sessions
3. Add the new user to `Administrators` group
4. Enable RDP in windows machine
5. Configure port forwarding in VirtualBox. Set up a rule to forward the RDP port (Default is `3389`) from the VM to the host
6. Install freerdp with flatpak:

    ```
    flatpak install flathub com.freerdp.FreeRDP
    ```
7. Test the rdp connection:

    ```
    flatpak run --command=xfreerdp --filesystem=host com.freerdp.FreeRDP /v:127.0.0.1 /u:rdp /p:rdp123 /cert:ignore
    ```
8. Enable Remote Apps by Modifying the Registry:

- 8.1 Save the following as a .reg file and execute it:
    ```
    Windows Registry Editor Version 5.00
        
        [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Terminal Server\TSAppAllowList]
        "fDisabledAllowList"=dword:00000001
    ```
- 8.2 Test a Remote App (e.g., File Explorer):

    ```
    flatpak run --command=xfreerdp com.freerdp.FreeRDP /v:127.0.0.1 /u:rdp /p:rdp123 /cert:ignore /app:"program:explorer.exe"
    ```

# Configuration

- Available in `~/.local/share/winapps_vbox/default.json`

    ```
    {
        "RDP":
        {
            "ip": "127.0.0.1",
            "port": "3389",
            "user": "rdp",
            "password": "rdp123"
        },

        "vbox": {
            "name": "win10"
        },

        "xfreerdp_cmd": [
            "flatpak",
            "run",
            "--command=xfreerdp",
            "com.freerdp.FreeRDP"
        ]
    }
    ```