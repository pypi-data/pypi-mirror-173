import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airnh",
    version="0.0.2",
    author="airnh",
    author_email="info@airnh.ca",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
            'numpy==1.23.4',
            'matplotlib==3.6.1',
            'websocket-client==1.4.1',
            'websockets==10.3',
      ],
)