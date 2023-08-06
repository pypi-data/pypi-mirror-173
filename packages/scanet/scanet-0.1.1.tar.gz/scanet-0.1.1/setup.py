from setuptools import setup, find_namespace_packages


setup(
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=['scanpy>=1.9.1','pyscenic>=0.11.2',"setuptools>=42","wheel"]
)