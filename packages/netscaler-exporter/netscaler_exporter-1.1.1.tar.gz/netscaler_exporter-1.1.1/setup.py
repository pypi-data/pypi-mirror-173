from netscaler_exporter.constants import (PKG_NAME, PKG_VERSION)
from setuptools import setup, find_packages

setup(
    name=PKG_NAME,
    version=PKG_VERSION,
    description='A Python-based Citrix Netscaler Exporter for Prometheus',
    long_description_content_type='text/markdown',
    long_description=open('README.md', 'r').read(),
    author="peekjef72",
    author_email="jfpik78@gmail.com",
    url="https://github.com/peekjef72/netscaler_exporter",
    entry_points={
        'console_scripts': [
            'netscaler_exporter = netscaler_exporter.netscaler_exporter:main',
            'build_netscaler_exporter_conf = netscaler_exporter.build_conf:main'
        ]
    },
    package_dir={"": "./"},
    packages=find_packages(where="./"),
    install_requires=open('./requirements.txt').readlines(),

    package_data={
        "netscaler_exporter": ["conf/*.yml", "conf/metrics/*.yml"],
    },
)

