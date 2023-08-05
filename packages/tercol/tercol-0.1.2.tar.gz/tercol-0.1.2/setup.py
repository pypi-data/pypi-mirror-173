from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setup(
    name="tercol",
    version="0.1.2",
    description="TerCol is a useless library that colors your text.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://butterroach.github.io/tercol/",
    author="Sultan Marzouq",
    author_email="epicnoobcontactemail@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="terminal styling, colors, style",
    packages=find_packages(),
    install_requires=[""],
    download_url="https://github.com/Butterroach/tercol/archive/refs/tags/v0.1.2.tar.gz",
)
