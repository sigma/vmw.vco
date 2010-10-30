from setuptools import setup, find_packages
import os
import sys

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if sys.version_info < (2, 7):
    setup_requires_version = ['unittest2']
else:
    setup_requires_version = []

setup(
    name = "vmw.vco",
    version = "0.3.1",
    license = "MIT",
    package_dir = {'': 'src'},
    packages = find_packages('src'),
    namespace_packages = ['vmw',],

    install_requires = ['vmw.ZSI',
                        'setuptools',
                        'zope.interface',
                        ],
    extra_requires = {'async': 'Twisted',
                      'doc': 'sphinx'},
    setup_requires = ['jinja2',
                      ] + setup_requires_version,

    description = "Python bindings for the VMware Orchestrator",
    long_description=read('README'),
    author = "VMware, Inc.",
    author_email = "yhodique@vmware.com",
    url = "http://sigma.github.com/vmw.vco",
    keywords = "vmware bindings",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        ],

    test_suite = 'unittest2.collector'
)
