from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

REPO_URL = "https://github.com/Geekeno/easy-env-var"
setup(
    name="easy_env_var",
    version="1.1.0",
    author="Geekeno",
    author_email="dev@geekeno.com",
    description="Simple util to get environment variables in the right data type.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=REPO_URL,
    packages=find_packages(exclude=["*.tests*"]),
    zip_safe=True,
    tests_require=["coverage[toml]"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    project_urls={
        "Documentation": REPO_URL,
        "Source": REPO_URL,
        "Tracker": f"{REPO_URL}/issues",
    },
)
