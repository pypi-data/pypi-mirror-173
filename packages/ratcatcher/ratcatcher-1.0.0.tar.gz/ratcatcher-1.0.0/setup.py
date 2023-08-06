import os
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, "README.md"), "r") as file:
    readme = file.read()

requirements = [
    "psutil==5.9.3",
    "scapy==2.4.5"
]


setup(
    name="ratcatcher",
    version="1.0.0",
    author="LLCZ00",
    description="Monitor and collect suspicious network traffic",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/LLCZ00/RATCatcher",
    license="Apache 2.0",
    keywords="malware analysis detection",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "ratcatcher=ratcatcher.ratcatcher:main",
            "omniserver=ratcatcher.omniserver:main"
        ]
    },
    python_requires=">=3.8",
    zip_safe=False,
    install_requires=requirements,
    packages=find_packages()
)
