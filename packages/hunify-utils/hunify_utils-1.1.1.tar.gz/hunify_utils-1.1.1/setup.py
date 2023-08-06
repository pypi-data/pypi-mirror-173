import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hunify_utils",
    version="1.1.1",
    author="Peter Tomek",
    author_email="tomek@hunifylabs.com",
    description="Hunify basic utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tom4c-hunify/hunify_utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)
