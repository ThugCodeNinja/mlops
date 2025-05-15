from setuptools import find_packages,setup

with (open('requirements.txt','r')) as f:
    req = f.read().splitlines()

setup(
    name="Hotel=reservation",
    version="0.1",
    author="Rutam Risaldar",
    packages=find_packages(),
    install_requires = req,
)