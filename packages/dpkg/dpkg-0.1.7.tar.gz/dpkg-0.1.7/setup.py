import setuptools

with open("README.md", "r", encoding='utf-8') as fn:
    long_description = fn.read()

setuptools.setup(
    name='dpkg',
    version='0.1.7',
    author='SangMinLee',
    author_email='smlee@d-if.kr',
    #package_dir={"":"src"},
    #py_modules=["apk"],
    packages=setuptools.find_packages(),
    #packages=find_packages(include=['src', 'metrics.*']),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
)

