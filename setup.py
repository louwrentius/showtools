import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="showtools",
        version="2.0.2",
        author="louwrentius",
        description="Show storage and network devices in table format on cli",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/louwrentius/showtools/", 
        packages=setuptools.find_packages(),
        install_requires=['rich'],
        include_package_data=True,
        package_data={},
        entry_points = {
            'console_scripts': [
                'show = showtools:main',
            ],
        },
        scripts=['bin/show'],
)
