import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spc-langchain",
    version="0.0.6",
    author="Arun Raja",
    author_email="arun.raja@skypointcloud.com",
    description="A package that contains shared python code and modules for all langchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arunraja1/langchain-improvement.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
    ],
)
