from setuptools import setup, find_packages
import os

setup(
    name = "pyvco",
    version = "0.1",
    packages = ['vmw.vco', 'vmw.vco.generated',],
    namespace_packages = ['vmw',],

    install_requires = ['vmw.ZSI',
                        'setuptools',
                        'Twisted',
                        ],
)
