# /usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='lrequest',
    version='0.0.1',
    description='Test model for upload pip to PyPi',
    long_description='',
    install_requires=[
        'aiohttp>=2.0.0',
        'cchardet>=2.0.0',
        'requests-html==0.10.0',
    ],
    author='Gar1and',
    author_email='garland_zhao@qq.com',
    license='MIT',
    url='https://github.com/web-trump/ahttp.git',
    platforms=["python 3.8+"],
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.8',
    ],
)
