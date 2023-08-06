
from setuptools import setup, find_namespace_packages
from pathlib import Path

try:
    long_description = (Path(__file__).parent / 'README.md').read_text(encoding='utf-8')
except FileNotFoundError:
    long_description = 'Readme missing'

setup(
    name="generalpackager",
    author='Rickard "Mandera" Abraham',
    author_email="rickard.abraham@gmail.com",
    version="0.5.6",
    description="Tools to interface GitHub, PyPI, NPM and local modules / repos. Used for generating files to keep projects dry and synced. Tailored for my general packages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'generallibrary[table]',
        'generalfile',
        'gitpython',
        'pygithub',
        'requests',
        'pyinstaller',
        'coverage',
    ],
    url="https://github.com/ManderaGeneral/generalpackager",
    license="mit",
    packages=find_namespace_packages(exclude=("build*", "dist*")),
    extras_require={},
    classifiers=[
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],
)
