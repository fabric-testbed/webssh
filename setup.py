import codecs
from setuptools import setup
from webssh._version import __version__ as version


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='webssh-bastion',
    version=version,
    description='Web based ssh client with bastion support',
    long_description=long_description,
    author='Shengdun Hua, modified by Ilya Baldin',
    author_email='webmaster0115@gmail.com',
    url='https://github.com/fabric-testbed/webssh',
    packages=['webssh-bastion'],
    entry_points='''
    [console_scripts]
    wssh = webssh.main:main
    ''',
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'tornado>=4.5.0',
        'paramiko>=2.3.1',
    ],
)
