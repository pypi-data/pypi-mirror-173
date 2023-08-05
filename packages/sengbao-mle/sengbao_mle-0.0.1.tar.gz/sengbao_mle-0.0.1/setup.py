__updated__ = "2022-10-24 00:33:39"

from setuptools import setup
import setuptools
import re
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name="sengbao_mle",
    version=get_version("sengbao_mle"),
    description="翻新的最大似然估计库 maximum likelihood estimation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="chenzongwei",
    author_email="winterwinter999@163.com",
    url="https://github.com/chen-001/sengbao_mle.git",
    # project_urls={"Documentation": "https://chen-001.github.io/pure_ocean_breeze/"},
    install_requires=["numpy", "scipy", "theano", "iminuit"],
    python_requires=">=3",
    license="MIT",
    packages=setuptools.find_packages(),
    requires=[],
)
