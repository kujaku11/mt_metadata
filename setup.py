#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "numpy",
    "scipy",
    "pandas",
    "matplotlib",
    "xarray",
    "loguru",
]

extras_require = {
        'obspy': ["obspy"],
        'test': ["pytest>=3"]
}

setup(
    author="Jared Peacock",
    author_email="jpeacock@usgs.gov",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Metadata for magnetotelluric data",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="mt_metadata",
    name="mt_metadata",
    packages=find_packages(include=["mt_metadata", "mt_metadata.*"]),
    test_suite="tests",
    url="https://github.com/kujaku11/mt_metadata",
    version="0.4.0",
    zip_safe=False,
    package_data={
        "": [
            "data/mt_xml/*.xml",
            "data/stationxml/*.xml",
            "data/transfer_functions/*.edi",
        ]
    },
    extras_require=extras_require,
)
