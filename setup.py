import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mspider",
    version="0.2.3",
    author="Tishacy",
    author_email="",
    description="Make your spider multi-threaded.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tishacy/MSpider",
    packages=setuptools.find_packages(),
    install_requires=["numpy>=1.14.4","requests>=2.18.4",
                      "pandas>=0.24.1","tqdm>=4.30.0",
                      "wget>=3.2","beautifulsoup4>=4.7.1"],
    entry_points={
        'console_scripts': [
            'genspider=mspider.genspider:genspider'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)