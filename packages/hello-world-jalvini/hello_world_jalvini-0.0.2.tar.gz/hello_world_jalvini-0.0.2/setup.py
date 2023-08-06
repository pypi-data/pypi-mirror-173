import setuptools as stpTool
from setuptools import setup

VERSION = "0.0.2"
DESCRIPTION = "Brown Advisory Wrapper"
PACKAGES = stpTool.find_packages()
setup(
    name="hello_world_jalvini",
    version=VERSION,
    author="Brown Advisory",
    author_email="jalvini@brownadvisory.com",
    description=DESCRIPTION,
    long_description="LONG_DESCRIPTION",
    long_description_content_type="text/markdown",
    url="https://github.com/need_to_add_repo_address",
    keywords=["python", "brown advisory"],
    py_modules=["hello_world"],
    packages= PACKAGES,
    include_package_data=True,  # use MANIFEST.in during install
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
