from pathlib import Path
from setuptools import setup, find_packages  # type: ignore[import]

long_description = Path("README.md").read_text()
reqs = Path("requirements.txt").read_text().strip().splitlines()

pkg = "grouvee_export"
setup(
    name=pkg,
    version="0.1.0",
    url="https://github.com/seanbreckenridge/grouvee_export",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description=("a partial grouvee exporter"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(include=[pkg]),
    install_requires=reqs,
    package_data={pkg: ["py.typed"]},
    zip_safe=False,
    keywords="",
    entry_points={"console_scripts": ["grouvee_export = grouvee_export.__main__:main"]},
    scripts=list(map(str, Path("bin").rglob("*"))),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
