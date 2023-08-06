from setuptools import setup

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="momlib",
    version="0.0.7",
    url="https://momlib.projects.b-roux.com//",
    author="B. Roux",
    description="Mathematical Object Manipulation Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD (3-Clause)",
    packages=[
        "momlib",
    ],
    keywords=[
        "library",
        "vector",
        "matrix",
        "mathematics",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
)
