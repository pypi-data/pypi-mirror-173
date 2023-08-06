import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ ="0.0.4"

REPO_NAME = "IPYNBRENDER"
AUTHOR_NAME = "EagleVector"
SRC_REPO = "IPYNBrender"
AUTHOR_EMAIL = "kumarsubhambili3@gmail.com"

setuptools.setup(
    name= SRC_REPO,
    version= __version__,
    author= AUTHOR_NAME,
    author_email= AUTHOR_EMAIL,
    description="A small python package that renders videos",
    long_description=long_description,
    long_description_content="text/markdown",
    url = f"https://github.com/{AUTHOR_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
