import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoRSA",
    version="0.0.1",
    author="Wu Xinyuan",
    author_email="1210011033@i.smu.edu.cn",
    description="A package for RSA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # exapmle
        'open3d',
        'numpy',
        'tqdm',
        'pyvista',
    ],
)