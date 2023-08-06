from setuptools import setup, find_packages

setup(
    name='spbstu-amml',
    packages=find_packages(),
    version='1.2.2',
    author='',
    description='modelhub',
    long_description='',
    url='',
    python_requires='>=3.8',
    install_requires=[
        "dvc[s3]>=2.27.2",
        "protobuf==3.19.5"
    ]
)