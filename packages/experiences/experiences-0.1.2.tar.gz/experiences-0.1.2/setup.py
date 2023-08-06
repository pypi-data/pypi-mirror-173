from setuptools import setup, find_packages

setup(
    author="Joe Chelladurai",
    description="Experience Research",
    name="experiences",
    version="0.1.2",
    packages=find_packages(include=["experiences", "experiences.*"]),
    install_requires=['pandas>=1.0', 'scipy==1.1'],
    python_requires='>=2.7, !=3.0.*, !=3.1*',
)