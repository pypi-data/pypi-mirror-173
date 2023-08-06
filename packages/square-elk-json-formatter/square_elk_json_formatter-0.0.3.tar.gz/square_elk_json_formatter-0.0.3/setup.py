from setuptools import setup, find_packages

__version__ = "0.0.3"

setup(
    name="square_elk_json_formatter",
    version=__version__,
    license="MIT",
    description="",
    url="https://github.com/UKP-SQuARE/square-elk-json-formatter",
    download_url=f"https://github.com/UKP-SQuARE/square-elk-json-formatter/archive/refs/tags/v{__version__}.tar.gz",
    author="UKP",
    author_email="baumgaertner@ukp.informatik.tu-darmstadt.de",
    packages=find_packages(),
    install_requires=["python-json-logger==2.0.1"]
)
