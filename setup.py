from setuptools import setup, find_packages
import os

setup(
    name = "vmw.vco",
    version = "0.1",
    package_dir = {'': 'src'},
    packages = find_packages('src'),
    namespace_packages = ['vmw',],

    install_requires = ['vmw.ZSI',
                        'setuptools',
                        'Twisted',
                        ],
)
