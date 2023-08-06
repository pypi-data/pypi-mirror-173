from setuptools import setup
setup(name = 'ssj',
version = '1.0.5',
author = 'Jonathan N. Nagel',
author_email = 'jinnascimento81@gmail.com',
requires = ['dropbox', 'tinydb', 'nested_dict', 'cryptography'],
packages = ['ssj'],
description = 'Servidor ou gestor de dados em JSON.',
license = 'MIT',
keywords = 'ssj')
