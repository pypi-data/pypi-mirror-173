from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'a random thing'

# Setting up
setup(
    name="pypim",
    version=VERSION,
    author="Mr Cottonball",
    author_email="<64mrnoah@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['none'],
    keywords=['python', 'math'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
