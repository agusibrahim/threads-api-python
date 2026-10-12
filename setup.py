from setuptools import setup, find_packages

setup(
    name="threads-api-python",
    version="1.0.0",
    description="Unofficial Python Automation Toolkit for Meta Threads Web API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Agus Ibrahim",
    url="https://github.com/agusibrahim/threads-api-python",
    packages=find_packages(),
    install_requires=[
        "curl_cffi>=0.7.0",
        "Pillow>=10.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
