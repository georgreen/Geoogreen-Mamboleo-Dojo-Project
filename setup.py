# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='officespaceallocation',
    version='0.1.0',
    description='Office Space Allocation System',
    long_description=readme,
    author='Georgreen Mamboleo Ngunga',
    author_email='geogreenmanu@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

