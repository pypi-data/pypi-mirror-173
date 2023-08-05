from setuptools import setup, find_packages
from Cython.Build import cythonize
import sys, os

with open('README.md', 'r') as fl:
    long_des = fl.read()

setup(
    name='SR29',
    version='1.0.3',
    author='Mame29',
    install_requires="progress",
    description='The SR29 encode and decode',
    long_description=long_des,
    long_description_content_type="text/markdown",
    ext_modules=cythonize(["sr29/SR29.c", "sr29/base.c"]),
    zip_safe=False,
    packages=find_packages(),
    package_data={'': ['LICENSE', 'NOTICE']},
    include_package_data=True,
    license="Apache License 2.0",
    entry_points={
        'console_scripts': [
            'SR29 = sr29:main'
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        ],
)
