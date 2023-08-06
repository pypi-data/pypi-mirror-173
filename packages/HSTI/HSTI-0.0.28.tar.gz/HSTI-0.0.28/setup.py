import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()


setuptools.setup(
    name="HSTI",
    version="0.0.28",
    author="Mads Nibe et. al.",
    author_email="mani@newtec.dk",
    description="The NEWTEC HSTI package contains fundamental functions for the data analysis of hyperspectral thermal images (HSTI).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={'': ['data_files/*.txt']},
    package_dir={"": "hsti-analysis"},
    packages=setuptools.find_packages(where="hsti-analysis"),
    python_requires=">=3.6",
    install_requires=install_requires,
)

