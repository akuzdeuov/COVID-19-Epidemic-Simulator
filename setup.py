#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 12:30:58 2020

@author: askat
"""
from setuptools import setup

setup(
    name='covid19_simulator',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'covid19_simulator=covid19_simulator:main'
        ]
    }
)
