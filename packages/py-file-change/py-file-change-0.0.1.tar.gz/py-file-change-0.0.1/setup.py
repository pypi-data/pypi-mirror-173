from setuptools import setup

with open("README.md","r") as f:
    long_description = f.read()

setup(
    name="py-file-change",
    version="0.0.1",
    description="py-file-change is a tool that execute specific command when any file changes in the directory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["python","file-change","file-events","reloader","python-file-change","command-reloader"],
    author="Harkishan Khuva",
    author_email="harkishankhuva02@gmail.com",
    url="https://github.com/hakiKhuva/py-file-change",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Topic :: System :: Filesystems",
        "Topic :: System :: Monitoring"
    ],
    package_dir={"py-file-change": "py-file-change"},
    packages=["py-file-change"],
    python_requires=">=3.8",
    license="MIT",
)