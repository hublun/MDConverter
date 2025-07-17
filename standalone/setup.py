"""
Setup script for MDConverter package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    with open(readme_file, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "A comprehensive Python toolkit for converting HTML webpage packages into clean, well-formatted Markdown files."

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    requirements = [
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0", 
        "markdownify>=0.11.6",
        "lxml>=4.9.0",
        "html5lib>=1.1"
    ]

setup(
    name="mdconverter",
    version="1.0.0",
    author="DRCEDU",
    description="HTML to Markdown Converter Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    entry_points={
        "console_scripts": [
            "mdconverter=mdconverter.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mdconverter": [
            "assets/templates/*.md",
            "assets/templates/*.html",
        ]
    },
)