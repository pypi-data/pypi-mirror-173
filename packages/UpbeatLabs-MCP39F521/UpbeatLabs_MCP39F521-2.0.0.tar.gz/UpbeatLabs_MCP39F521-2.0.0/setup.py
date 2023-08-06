#!/usr/bin/env python
import os
import io
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development',
    'Topic :: System :: Hardware'
    ]

setup(name='UpbeatLabs_MCP39F521',
      version='2.0.0',
      description='Python library to use with Dr. Wattson Energy Monitoring Board and other MCP39F521 based boards',
      long_description=long_description,
      author='Sridhar Rajagopal',
      author_email='sridhar@upbeatlabs.com',
      url='https://github.com/upbeatlabs/UpbeatLabs_Python_MCP39F521',
      license = 'BSD License',
      classifiers = classifiers,
      packages=['UpbeatLabs_MCP39F521'],
      install_requires=[
          'smbus2',
          ]
     )
