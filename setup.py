from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nba_stats_tracking",
    version="1.0.6",
    author="Darryl Blackport",
    author_email="darryl.blackport@gmail.com",
    description="A package to work with NBA player tracking stats using the NBA Stats API",
    license="MIT License",
    keywords=["basketball", "NBA", "player tracking"],
    url="https://github.com/dblackrun/nba-stats-tracking",
    packages=find_packages(),
    install_requires=["requests", "python-dateutil", "pydantic"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
