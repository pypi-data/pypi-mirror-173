from pathlib import Path
import setuptools


# essential for every package, it needs to have a unique name
setuptools.setup(
    name="IndigoFranzpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.setuptools.find_packages(exclude=["tests", "data"])
)
