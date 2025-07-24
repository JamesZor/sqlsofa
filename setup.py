from setuptools import find_packages, setup

setup(
    name="sqlsofa-package",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "omegaconf>=2.3.0",
    ],
    package_data={
        "sqlsofa": ["conf/**/*.yaml"],
    },
    include_package_data=True,
    author="James",
    description="Handle sql side of the data",
)
