from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'test pkg'

# Setting up
setup(
    name="giangitestpkg",
    version=VERSION,
    author="Gianluca",
    author_email="<viogianluca77@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['wheel'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)