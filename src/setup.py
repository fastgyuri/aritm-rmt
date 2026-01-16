from setuptools import setup, find_packages

setup(
    name="prime-gaps-research",
    version="1.0.0",
    author="Gheorghe Robert Cîmpeanu",
    author_email="your.email@example.com",
    description="Empirical analysis of maximal prime gaps",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/[username]/prime-gaps-research",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.5.0",
        "scipy>=1.7.0",
        "seaborn>=0.11.0",
        "requests>=2.26.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
        "notebook": [
            "jupyter>=1.0.0",
            "ipykernel>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "prime-gaps=run_analysis:main",
        ],
    },
)
