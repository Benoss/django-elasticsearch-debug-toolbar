from setuptools import find_packages
from distutils.core import setup

setup(
    name="django-elasticsearch-debug-toolbar",
    packages=find_packages(),
    version="2.0.0",
    description="A Django Debug Toolbar panel for Elasticsearch",
    long_description=open("README.md").read(),
    author="Benoit Chabord",
    author_email="benauf@gmail.com",
    url="http://github.com/Benoss/django-elasticsearch-debug-toolbar",
    license="MIT",
    keywords=["django", "es", "elastic", "elasticsearch"],
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    tests_require=["nose", "django-debug-toolbar", "elasticsearch"],
    test_suite="nose.collector",
)
