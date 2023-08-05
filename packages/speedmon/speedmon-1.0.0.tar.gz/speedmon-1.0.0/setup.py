from setuptools import setup, find_packages

with open("README.md", "r") as r:
    desc = r.read()

setup(
    name="speedmon",            
    version="1.0.0",
    author="5f0",
    url="https://github.com/5f0ne/speedmon",
    description="Performance Monitoring Capabilities",
    classifiers=[
        "Operating System :: OS Independent ",
        "Programming Language :: Python :: 3 ",
        "License :: OSI Approved :: MIT License "
    ],
    license="MIT",
    long_description=desc,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    install_requires=[
        
    ],
     entry_points={
        "console_scripts": [
            "speedmon = speedmon.__main__:main"
        ]
    }
)
