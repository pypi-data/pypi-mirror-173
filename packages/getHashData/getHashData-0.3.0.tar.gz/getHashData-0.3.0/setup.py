# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='getHashData',
    version='0.3.0',
    author='th35tr0n9',
    author_email='th35tr0n9@gmail.com',
    url='https://hxzy.me',
    description=u'Simple way to get functions or events hash or sign a message.',
    long_description=open('README.rst', encoding='utf-8').read(),
    packages=['getHashData'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'getHash=getHashData:main',
        ]
    }
)