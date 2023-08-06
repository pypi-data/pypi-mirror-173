#!/usr/bin/env python3

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()


setup(
    name='tmx-nano-2040-wifi-aio',
    packages=['tmx_nano2040_wifi_aio'],
    install_requires=['pyserial'],

    version='1.1',
    description="Remotely Control An Arduino Nano RP2040 Connect",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Alan Yorinks',
    author_email='MisterYsLab@gmail.com',
    url='https://github.com/MrYsLab/tmx-nano-2040-wifi-aio',
    download_url='https://github.com/MrYsLab/tmx-nano-2040-wifi-aio',
    keywords=['telemetrix', 'Arduino', 'Protocol', 'Python'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

