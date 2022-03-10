# pylint: disable=open-builtin
from __future__ import absolute_import, print_function, unicode_literals

import os

from setuptools import find_packages, setup
from version import __version__

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns:
        list: Requirements file relative path strings
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split("#")[0].strip() for line in open(path).readlines() if is_requirement(line.strip())
        )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement.
    Returns:
        bool: True if the line is not blank, a comment, a URL, or an included file
    """
    return not (
        line == ""
        or line.startswith("-c")
        or line.startswith("-r")
        or line.startswith("#")
        or line.startswith("-e")
        or line.startswith("git+")
    )


README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()
CHANGELOG = open(os.path.join(os.path.dirname(__file__), "CHANGELOG.rst")).read()

print("Found packages: {packages}".format(packages=find_packages()))

print("requirements found: {requirements}".format(requirements=load_requirements("requirements/common.in")))

setup(
    name="example-plugin",
    version=__version__,
    packages=find_packages(),
    package_data={"": ["*.html"]},  # include any Mako templates found in this repo.
    include_package_data=True,
    license="Proprietary",
    description="Django plugin to enhance feature set of base Open edX platform.",
    long_description="",
    author="Lawrence McDaniel",
    author_email="lpm0073@gmail.com",
    url="https://github.com/Turn-The-Bus/example-openedx-plugin",
    install_requires=load_requirements("requirements/common.in"),
    zip_safe=False,
    keywords="Django, Open edX, example",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        # mcdaniel feb-2022
        #
        # IMPORTANT: ensure that this entry_points coincides with that of edx-platform
        #            and also that you are not introducing any name collisions.
        # https://github.com/openedx/edx-platform/blob/master/setup.py#L88
        "lms.djangoapp": [
            "openedx_plugin = openedx_plugin.apps:StepwisePluginConfig",
        ],
        "cms.djangoapp": [],
    },
    extras_require={
        "Django": ["Django>=2.2,<2.3"],
    },
)
