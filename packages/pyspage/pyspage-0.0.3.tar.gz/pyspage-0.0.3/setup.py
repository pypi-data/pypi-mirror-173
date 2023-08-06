from setuptools import setup, find_packages
import sys
sys.path.append('./pyspage')
from pyspage import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyspage',
    version=__version__,
    description='Quickly build open source web pages for academic purposes in a pythonic and elegant way.',
    url='https://github.com/chunribu/pyspage/',
    author='Jian Jiang',
    author_email='jianjiang.bio@gmail.com',
    packages=find_packages(),
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={},
    include_package_data=False,
    install_requires=[],
    entry_points = {
        'console_scripts': ['pyspage=pyspage.command:run'],
    },
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='pyscript pywebio shiny',
)