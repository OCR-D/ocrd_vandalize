# -*- coding: utf-8 -*-
import codecs
import json

from setuptools import setup, find_packages

# 
with codecs.open('README.md', encoding='utf-8') as f:
    README = f.read()
with open('./ocrd-tool.json', 'r') as f:
    version = json.load(f)['version']

setup(
    name='ocrd_vandalize',
    version=version,
    description='Demo processor to illustrate the OCR-D Pytonn API',
    long_description=README,
    long_description_content_type='text/markdown',
    author='OCR-D',
    author_email='info@ocr-d.de',
    url='https://github.com/OCR-D/ocrd_vandalize',
    license='Apache License 2.0',
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    package_data={
        '': ['*.json', '*.ttf'],
    },
    entry_points={
        'console_scripts': [
            'ocrd-vandalize=ocrd_vandalize.ocrd_cli:cli',
        ]
    },
)
