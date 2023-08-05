#!/usr/bin/env python3

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='kiddeelab',
    #packages=['kiddeejoystick', 'kiddeemata', 'gamepad'],
    py_modules=['kiddeejoystick', 'kiddeemata', 'gamepad'],
    install_requires=['pyserial', 'Pillow', 'pygame'],

    version='0.0.1.dev1',
    description="Kiddee Lab modules, including a Python Library To Read Data From the Kiddee Joystick and a Python Protocol Abstraction Library For Arduino Firmata - Updated by Kiddee Lab",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Kiddee Lab',
    author_email='kiddeelab2@gmail.com',
    url='https://github.com/xavjb/kiddeejoystick',
    download_url='https://github.com/xavjb/kiddeejoystick',
    keywords=['Firmata', 'Serial Port', 'Arduino', 'Python', 'Protocol', 'Python', 'Kiddee Lab', 'Joystick', 'Gamepad'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)