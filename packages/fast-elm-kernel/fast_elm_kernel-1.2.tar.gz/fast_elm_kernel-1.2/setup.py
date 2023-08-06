from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="fast_elm_kernel",
    description="Extreme Learning Machine kernels for ML",
    version="1.2",
    install_requires=["numpy"],
    packages=["fast_elm_kernel"],
    long_description_content_type="text/markdown",
    long_description=long_description
)