import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libsocket",
    version="1.31.0",
    author="Chaxiraxi - nem013",
    author_email="ChaxiraxiCH@protonmail.ch",
    description="A socket library that facilitates communication between python client and server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Les-Venogeois/libsocket",
    packages=setuptools.find_packages(),
    install_requires=['pycryptodome'],
    package_data={"libsocket": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)