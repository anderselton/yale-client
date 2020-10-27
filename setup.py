import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='yaleclient',
    py_modules=['yaleclient'],
    version='0.2.2',
    entry_points={
        "console_scripts": ['yale-cli = yaleclient.cli:main']
    },
    description='Interact with Yale systems',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Anders Elton',
    url='https://github.com/anderselton/yale-client',
    download_url='https://github.com/anderselton/yale-client',
    keywords=['alarm', 'Yale', 'Smart Alarm', 'Lock', 'doorman'],
    package_data={'': ['data/*.json']},
    install_requires=['requests>=2.0.0', 'backoff>=1.10.0'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
