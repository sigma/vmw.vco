from setuptools import setup, find_packages
import os

setup(
    name = "vmw.vco",
    version = "0.3.1",
    license = "MIT",
    package_dir = {'': 'src'},
    packages = find_packages('src'),
    namespace_packages = ['vmw',],

    install_requires = ['vmw.ZSI',
                        'setuptools',
                        'Twisted',
                        ],

    description="Python bindings for the VMware Orchestrator",
    author="Yann Hodique",
    author_email="yhodique@vmware.com",
    url="http://sigma.github.com/vmw.vco",

)
