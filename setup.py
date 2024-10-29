from setuptools import setup, find_packages

setup(
    name="nurral",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,  # Include non-Python files
    package_data={
        'nurral': ['csv/*.csv',
                         ],  # Adjust the path to your files
    },
    description="A financial data extractor",
    author="Simulation Coder",
    author_email="brain@nurral.com",
    url="https://github.com/simulationcoder/nurral",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12.5",

    install_requires=[
            "logging>=0.4.9.6"
            "numpy>=2.1.2",
            "pandas>=2.2.3",
            "python-dateutil>=2.9.0.post0",
            "setuptools>=75.2.0",
            "six==1.16.0",
            "tzdata==2024.2",
    ],
)