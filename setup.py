#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
from setuptools import setup, find_packages

ver = '2.1.paperlabs'
README = os.path.join(os.path.dirname(__file__), 'README.rst')
long_desc = open(README).read() + '\n\n'

setup(name='pyga',
      version=ver,
      author='Arun K.R.',
      author_email='the1.arun@gmail.com',
      url='https://github.com/kra3/py-ga-mob',
      license='Simplified BSD',
      description='Server side implemenation of Google Analytics in Python.',
      long_description=long_desc,
      keywords='google analytics  mobile serverside',
      requires=[],
      install_requires=['setuptools',],
      packages=find_packages(),
      namespace_packages=['pyga'],
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
      ],
)
