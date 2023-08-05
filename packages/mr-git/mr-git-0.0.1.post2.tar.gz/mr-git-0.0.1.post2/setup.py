"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""

from setuptools import setup, find_packages
import pathlib

VERSION = "0.0.1.post2"

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="mr-git",
    version=VERSION,
    description="Multi-Repositories Git tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pbauermeister/mr-git",
    author="Pascal Bauermeister",
    author_email="pascal.bauermeister@gmail.com",
    classifiers=[
        # https://pypi.org/classifiers/ :
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Version Control",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
    keywords="diagram-generator, development, tool",
    license="GNU General Public License v3 (GPLv3)",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10, <4",
    install_requires=["svgwrite", "svglib"],
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    package_data={
    },
    # The following would provide a command called `mr-git` which
    # executes the function `main` from this package when invoked:
    entry_points={
        "console_scripts": [
            "mr-git=mr_git:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/pbauermeister/mr-git/issues",
#        "Funding": "https://donate.pypi.org",
#        "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https://github.com/pbauermeister/mr-git",
    },
)
