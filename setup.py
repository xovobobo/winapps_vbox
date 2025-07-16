import os

from setuptools import find_packages, setup
from glob import glob

apps_path = os.path.relpath(
    os.path.join(
        os.path.dirname(__file__),
        "winapps_vbox",
        "apps"
    )
)


all_desktops_exe = glob( os.path.join(apps_path, "**/*.desktop"), recursive=True)
all_desktops_icons = glob( os.path.join(apps_path, "**/*.svg"), recursive=True)


setup(
    name="winapps_vbox",
    packages=find_packages(),
    version="0.0.1",
    entry_points = {
        "console_scripts":
            [
                "winapps_launch=winapps_vbox.launcher:main"
            ]
    },
    package_data={
        'winapps_vbox': ['config/default.json']
    },
    data_files=[
        ('share/applications', all_desktops_exe),
        ('share/icons', all_desktops_icons),
        ('share/winapps_vbox', ['winapps_vbox/config/default.json']),
    ]
)