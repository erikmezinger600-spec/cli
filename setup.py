#!/usr/bin/env python3
"""
PCSploit — Post-Exploitation C2 Framework
Authorized Penetration Testing Tool

Installation:
    pip install -e .
    python setup.py install
"""
from setuptools import setup, find_packages
import os

# Read the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="pcsploit",
    version="1.0.0",
    author="PCSploit Team",
    author_email="dev@pcsploit.io",
    description="Post-Exploitation C2 Framework for Authorized Penetration Testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/PCSploit",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/PCSploit/issues",
        "Documentation": "https://github.com/yourusername/PCSploit/wiki",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pcsploit=pcsploit.server:main",
            "pcsploit-generate=pcsploit.generator:main",
        ],
    },
    package_data={
        "pcsploit": [
            "modules/*.py",
            "templates/*.py",
        ],
    },
    zip_safe=False,
)
