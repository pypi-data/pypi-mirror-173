import setuptools

#with open("readme.md", "r") as fh:
    #long_description = fh.read()

setuptools.setup(
    name="TempConverter",
    version="0.9",
    author="Akash",
    author_email="akash9129@gmail.com",
    description="A small package to convert temperature",
    long_description='A Package to convert temperature',
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)