import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open("README.md", "r") as fh:
    long_description =fh.read()

setup(
    name = "ulpsych",
    version = "0.0.0.1",
    author = "Kevin O'Malley",
    author_email = "kevin.omalley@ul.ie",
    description = ('''A tool for helping people with administration tasks, with a focus on grading admin and module setup'''),
    license = "GNU GPL",
    py_modules=['Module', 'Assignment', ],
    erl = "https://github.com/spider-z3r0/grading_colation",
    package_dir={'':'src'},
    long_description= long_description,
    long_description_content_type = 'text/markdown',
    extras_require = {
        "dev" :[
            "pytest>=3.7",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)