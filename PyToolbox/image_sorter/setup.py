import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Image Sorter-Manu", # Replace with your own username
    version="0.0.1",
    author="Manuel Gonzalez-Rivero",
    author_email="m.gonzalezrivero@aims.gov.au",
    description="A small package for LTMP 3D surverys to help sorting timelapse images into SiteXXTranXX folders. It uses timegaps to closter images into subdirectories and QR scanner to rename folders",
    long_description=long_description,
    long_description_content_type="text",
    url="https://github.com/AIMS/reef3D/tree/master/PyToolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)