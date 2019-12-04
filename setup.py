from setuptools import setup
from setuptools import find_packages
from distutils.core import Command
import subprocess
import sys

with open('requirements.txt') as f:
    install_reqs = f.readlines()
    reqs = [str(ir) for ir in install_reqs]


class InstallCommand(Command):
    description = "Installs MerkleProof2019."

    def run(self):
        install(reqs)


def install(packages):
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


setup(
    name='lds-merkle-proof-2019',
    version='0.0.1',
    packages=find_packages(),
    install_requires=reqs,
    url='',
    license='',
    author='anthonyronning',
    author_email='aronning@learningmachine.com',
    description='MerkleProof2019 module for python'
)
