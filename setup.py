from setuptools import setup, find_packages

setup(
    name="weather_analysis_in_major_US_cieis_2024",
    version="0.1.0",
    packages=find_packages(), # automatically find packages
    install_requires=["pandas", "numpy"],
    author="Mingi Cooper Song",
    author_email="10835225@uvu.edu",
    description="A package for calculating descriptive statistics",
    long_description=open(r"C:\Users\msong\OneDrive\Documents\cs3270/readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/msong1342/CS3270_UVU_Projects.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)