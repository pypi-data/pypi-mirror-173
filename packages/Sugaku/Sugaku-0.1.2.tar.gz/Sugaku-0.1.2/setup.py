from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.1.2'
DESCRIPTION = 'Python module to generate a calculation chain.'

# Setting up
setup(
    name="Sugaku",
    version=VERSION,
    author="ZeyaTsu",
    author_email="zeyatsou@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'math', 'mathematics', 'maths', 'calculus', 'calculations'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)