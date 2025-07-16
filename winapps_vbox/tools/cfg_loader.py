import json

from dataclasses import dataclass
from typing import List

@dataclass 
class VboxCfg:
    name: str

@dataclass
class RdpCfg:
    ip: str
    port: int
    user: str
    password: str


@dataclass
class Config:
    rdp: RdpCfg
    xfreerdp_cmd: List[str]
    vbox: VboxCfg

    @classmethod
    def from_json_file(cls, file_path: str):
        with open(file_path, 'r') as f:
            cfg_data = json.load(f)

        rdpcfg = RdpCfg(
            ip = cfg_data['RDP']['ip'],
            port = cfg_data['RDP']['port'],
            user = cfg_data['RDP']['user'],
            password = cfg_data['RDP']['password']
        )

        return cls(
            rdp = rdpcfg,
            xfreerdp_cmd = cfg_data['xfreerdp_cmd'],
            vbox = VboxCfg(name=cfg_data['vbox']['name'])
        )

if __name__ == "__main__":
    cfg = Config.from_json_file('/home/bobo/Projects/rdp/winapp_vbox/config/default.json')
    print('qq')