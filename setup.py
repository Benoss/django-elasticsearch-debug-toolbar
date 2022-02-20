from distutils.core import setup

from setuptools import find_packages

setup(
    name="django-elasticsearch-debug-toolbar",
    packages=find_packages(),
    version="3.0.2",
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    tests_require=["pytest", "django-debug-toolbar", "elasticsearch"],
    test_suite="pytest.collector",
)
