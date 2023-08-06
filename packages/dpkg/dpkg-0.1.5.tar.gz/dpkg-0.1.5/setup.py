from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fn:
    long_description = fn.read()

setup(
    name='dpkg',
    version='0.1.5',
    author='SangMinLee',
    author_email='smlee@d-if.kr',
    #package_dir={"":"src"},
    #py_modules=["apk"],
    packages=find_packages(),
    #packages=find_packages(include=['src', 'metrics.*']),
    long_description=long_description,
    long_description_content_type="text/markdown"
)

