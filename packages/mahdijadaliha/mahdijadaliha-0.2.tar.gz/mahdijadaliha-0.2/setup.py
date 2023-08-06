#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='mahdijadaliha',
    version='0.2',
    description='highlights keywords syntax, and use template files to generate code',
    url='https://db2sql.com/snippy',
    author='Mahdi Jadaliha',
    author_email='jadaliha@gmail.com',
    license='MIT',
    py_modules = ['mahdijadaliha','mahdijadaliha.src.template'],
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('templates', ['mahdijadaliha/data/sql_templates.sql']),
        ('keywords', ['mahdijadaliha/data/sql_keywords.txt'])
    ],
    zip_safe=False)