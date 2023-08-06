import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MacToManufacturer",
    version="0.1.0",
    author="Nishant Bhandari",
    author_email="getrooted0019@hotmail.com",
    description="Library to find manufacturer of a device using macaddress.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/n1snt/MacToManufacturer",
    project_urls={
        "Bug Tracker": "https://github.com/n1snt/MacToManufacturer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={'': ['data/manuf.csv']},
    python_requires=">=3.6",
)