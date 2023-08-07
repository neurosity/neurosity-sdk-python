from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='neurosity',
    py_modules=['neurosity'],
    packages=find_packages(),
    version='2.1.1',
    url='https://github.com/neurosity/neurosity-sdk-python',
    python_requires='>=3.8',
    description='Official Neurosity Python SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alex Castillo',
    license='MIT',
    install_requires=['firebase-rest-api'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
