#!/usr/bin/env python
# -*- coding: utf8 -*-

import setuptools


setuptools.setup(
    name="zeeguu",
    version="0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    author="Simon Marti",
    author_email="marti.simon@students.unibe.ch",
    description="API for Zee Guu project",
    keywords="second language acquisition api zee guu",
    dependency_links=('http://github.com/zacharyvoase/cssmin/'
                      'tarball/master#egg=cssmin-0.1.4',),
    install_requires=("flask", "Flask-SQLAlchemy", "Flask-Assets",
                      "cssmin", "jsmin", "flask-wtf")
)
