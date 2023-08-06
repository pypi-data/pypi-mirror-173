#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-pingguo-pytest-plugin',
    version='0.1.0',
    author='wessonlan',
    author_email='wessonsang@163.com',
    maintainer='wessonlan',
    maintainer_email='wessonsang@163.com',
    license='Mozilla Public License 2.0',
    url='https://github.com/wessonlan/pytest-pingguo-pytest-plugin',
    description='pingguo test',
    py_modules=['pytest_pingguo_pytest_plugin'],
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    ],
    entry_points={
        'pytest11': [
            'pingguo-pytest-plugin = pytest_pingguo_pytest_plugin',
        ],
    },
)
