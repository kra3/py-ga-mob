#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
from setuptools import setup, find_packages


README = os.path.join(os.path.dirname(__file__), 'README.rst')
long_desc = open(README).read() + '\n\n'

setup(name='pyga',
      version='2.5.2',
      license='Simplified BSD',
      author='Arun K.R.',
      author_email='the1.arun@gmail.com',
      url='http://kra3.github.com/py-ga-mob/',
      description='Server side implemenation of Google Analytics in Python.',
      long_description=long_desc,
      keywords='google analytics  mobile serverside',
      install_requires=['setuptools', 'six'],
      packages=find_packages(),
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
      ],
      test_suite='tests',
      tests_require=['mock', 'six',]
    )
