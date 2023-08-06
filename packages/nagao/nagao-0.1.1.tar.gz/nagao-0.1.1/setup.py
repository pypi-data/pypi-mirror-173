import setuptools
import os

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(CUR_DIR, "README.md")
with open("README.md", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="nagao",
    version="0.1.1",
    description="Counting word frequency based on Nagao algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chiang97912/nagao",
    author="Chiang97912",
    author_email="chiang97912@gmail.com",
    packages=["nagao"],
    scripts=["scripts/nagao"],
    include_package_data=True,
    install_requires=[
        "click>=7.1.2",
        "nltk>=3.5",
        "sqlite_utils>=3.26.1",
        "ext_sort>=0.2.0"
    ],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ),

    keywords='nagao'
)
