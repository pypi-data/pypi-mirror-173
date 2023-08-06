import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airnh",
    version="0.0.4",
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
            'control==0.9.2',
            'matplotlib==3.6.1',
            'websocket-client==1.4.1',
            'websockets==10.3',
            'pandas==1.5.1',
            'ipywidgets',
            'jupyter',
            'jupyterlab',
            'notebook',
            'voila==0.3.6',
            'ipympl',
            'ipykernel',
            'scipy==1.9.3',
            'opencv-contrib-python==4.6.0.66',
            'opencv-python==4.6.0.66',
            'scikit-learn==1.1.2',
            'pathlib==1.0.1',
            'Pillow==9.2.0',
            'image',
            'pyserial==3.5',
            'pysound==0.2',
      ],
)