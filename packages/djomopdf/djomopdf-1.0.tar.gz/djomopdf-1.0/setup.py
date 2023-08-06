import setuptools
from pathlib import Path

readme_content = "Djomo PDF"

if Path("README.md").exists:
    readme_content = Path("README.md").read_text()

setuptools.setup(
    name="djomopdf", # unique name for a  package to avoid conflict with other packages
    version=1.0,
    long_description=readme_content, # we will come back hier later
    packages=setuptools.find_packages(exclude=["tests", "data"]) # tell what package are going to be distributed
)
