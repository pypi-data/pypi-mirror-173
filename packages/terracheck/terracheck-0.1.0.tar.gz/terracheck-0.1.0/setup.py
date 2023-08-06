#!/usr/bin/env python

from asyncore import read
from setuptools import setup, find_packages

# Reading long description from file
with open('README.md') as file:
    long_description = file.read()

# Specify requirements of your package here
REQUIREMENTS = [
    'python-hcl2==3.0.5',
    'colorama==0.4.5',
    'pytest==7.2.0',
    'PyYAML==6.0'
  ]

# Some more details
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    ]

setup(name='terracheck',
      version='0.1.0',
      description='Python Terraform checker from GCP good practices',
      long_description=long_description,
      long_description_content_type="text/markdown",
      #url='https://github.com/nikhilkumarsingh/mygmap',
      author='William Attache',
      author_email='william.attache@mydevacademy.com',
      license='MIT',
      packages=find_packages(exclude=('tests', 'docs')),
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='terraform gcp goodpractices'
     )