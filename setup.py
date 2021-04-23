from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python_socket_server_example',
    version='1.0',
    description='Program that implements a service listening in a socket.',
    long_description=long_description,

    url='https://github.com/loski07/aid_template_engine',
    author='Pablo Díaz <loski07@gmail.com>',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Recruiting',
        'Programming Language :: Python :: 3.9'
    ],

    keywords='template_engine',

    packages=find_packages(exclude=['engine', 'docs', 'tests']),

    install_requires=[],

    entry_points={
        'console_scripts': [
            'socket_server_example = server.server:main',
        ],
    }
)
