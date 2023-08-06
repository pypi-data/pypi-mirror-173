from setuptools import setup

requirements = ['requests']

setup(
    name="rayyan_store",
    version="0.1.1",
    description="Python client interface for RayyanStore",
    author="Fadhil Abubaker",
    packages=['rayyan_store'],
    install_requires=requirements
)
