import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="npd-fs-data",
    version="0.0.4",
    author="Max Leonard",
    author_email="maxhleonard@gmail.com",
    description="Library for easy programatic access Financial Services info",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://NPDGroup@dev.azure.com/NPDGroup/NPDFinancialServices/_git/WhaleWisdom",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src","NpdFsData":"src/NpdFsData"},
    packages=["NpdFsData"],
    python_requires=">=3.6",
    install_requires = [
        "azure-storage-blob",
        "azure-data-tables",
        "pandas"
    ]
)