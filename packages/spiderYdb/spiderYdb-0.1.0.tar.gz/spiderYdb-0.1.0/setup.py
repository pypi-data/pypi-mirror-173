from setuptools import find_packages, setup
setup(
    name='spiderYdb',
    packages=find_packages(include=['spiderYdb']),
    version='0.1.0',
    description='My first ORM for work with YDB',
    author='Vyacheslav Linnik',
    license='MIT',
    setup_requires="ydb==2.10.0",
)