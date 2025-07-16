import argparse
import os
import subprocess
import pkg_resources

from pathlib import PureWindowsPath
from typing import List
from winapps_vbox.tools.cfg_loader import Config
from winapps_vbox.tools.vbox_api import get_running_machines, start_machine, stop_machine
from winapps_vbox.tools.lsof import get_active_rdp_connections


class Launcher:
    def __init__(self) -> None:
        try:
            cfg_path = pkg_resources.resource_filename('winapps_vbox', 'config/default.json')
            print(f'load user config file from: {cfg_path}')
            self.cfg = Config.from_json_file(cfg_path)
        except Exception as e:
            print(f'Failed to load user config file. Error: {e}')
            print(f'Load default config')

            cfg_path = os.path.join( os.path.dirname(__file__), "config", "default.json")
            self.cfg = Config.from_json_file(cfg_path)
        
        self.cfg.xfreerdp_cmd.append(f'/v:{self.cfg.rdp.ip}:{self.cfg.rdp.port}')
        self.cfg.xfreerdp_cmd.append(f'/u:{self.cfg.rdp.user}')
        self.cfg.xfreerdp_cmd.append(f'/p:{self.cfg.rdp.password}')
        self.cfg.xfreerdp_cmd.append(f'/drive:share,{os.environ["HOME"]}',)
        self.cfg.xfreerdp_cmd.append(f'/cert:ignore')

    def start_rdp(self):
        self.__execute_command(self.cfg.xfreerdp_cmd)

    def start_rdp_app(self, program:str, document_path: str):
        command = self.cfg.xfreerdp_cmd.copy()
        command.append('/multimon')
        command.append('/span')

        if not (os.path.isabs(document_path)):
            document_path = os.path.join(os.getcwd(), document_path)

        document_path = os.path.normpath(document_path.replace(os.environ["HOME"], ''))
        document_path = document_path.lstrip('/\\')

        prog_path = PureWindowsPath(r"\\tsclient\share") / document_path

        app_param = f'/app:program:{program},cmd:"{prog_path}"'
        command.append(app_param)
        self.__execute_command(command)

    def __execute_command(self, command: List[str]):
        if self.cfg.vbox.name not in get_running_machines():
            print("Starting machine...")
            start_machine(self.cfg.vbox.name)

        print("Executing command:", ' '.join(command))
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running FreeRDP: {e}")
        finally:
            if get_active_rdp_connections(self.cfg.rdp.ip, self.cfg.rdp.port) == 0:
                print("Stopping machine...")
                stop_machine(self.cfg.vbox.name)


def main():
    parser = argparse.ArgumentParser(description='Winapps launcher')
    parser.add_argument("program", type=str, nargs='?', help="Program name. (example: WINWORD.exe)")
    parser.add_argument("document_path", type=str, nargs='?', help="Relative or absolute document path (example: test.docx)")

    args = parser.parse_args()

    launcher = Launcher()

    if args.program is None and args.document_path is None:
        launcher.start_rdp()
    else:
        launcher.start_rdp_app(program=args.program, document_path=args.document_path)


if __name__ == "__main__":
    main()