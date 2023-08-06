import setuptools

with open("README.md", "r") as fhandle:
    long_description = fhandle.read()
setuptools.setup(
    name="wscrape", 
    version="0.0.1", 
    author="Crow Randalf", 
    author_email="somethings8596@gmail.com", 
    description="A small package that allows you to quickly scrape things off the web.", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GoodMusic8596/wscrape", 
    packages=setuptools.find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], 
		instal_requires = ["bs4 >= 0.0.1"],
    python_requires='>=3.8',
)