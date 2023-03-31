# coding=utf-8
"""
Lawrence McDaniel https://lawrencemcdaniel.com

The style and organizational scheme for this setup.py is largely copied from
these two projects:
        openedx: https://github.com/openedx/edx-platform/blob/master/setup.py
        tutor: https://github.com/overhangio/tutor/blob/master/setup.py
"""
# pylint: disable=open-builtin
import io
import os
from setuptools import find_packages, setup
from typing import Dict, List

HERE = os.path.abspath(os.path.dirname(__file__))

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def load_readme() -> str:
    with io.open(os.path.join(HERE, "README.md"), "rt", encoding="utf8") as f:
        readme = f.read()
    # Replace img src for publication on pypi
    return readme.replace(
        "./doc/",
        "https://github.com/cookiecutter-openedx/cookiecutter-openedx-devops/raw/main/doc/",
    )


def load_about() -> Dict[str, str]:
    about: Dict[str, str] = {}
    with io.open(os.path.join(HERE, "__about__.py"), "rt", encoding="utf-8") as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


def load_requirements(*requirements_paths) -> List[str]:
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


def is_requirement(line) -> bool:
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
CHANGELOG = open(os.path.join(os.path.dirname(__file__), "CHANGELOG.md")).read()
ABOUT = load_about()

print("Found packages: {packages}".format(packages=find_packages()))
print("requirements found: {requirements}".format(requirements=load_requirements("requirements/common.in")))

setup(
    name="example-plugin",
    version=ABOUT["__package_version__"],
    packages=find_packages(),
    package_data={"": ["*.html"]},  # include any Mako templates found in this repo.
    include_package_data=True,
    license_files=("LICENSE.txt",),
    license="AGPLv3",
    description="Django plugin to enhance feature set of base Open edX platform.",
    long_description=load_readme(),
    author="Lawrence McDaniel",
    author_email="lpm0073@gmail.com",
    url="https://github.com/cookiecutter-openedx/example-openedx-plugin",
    download_url=("https://github.com/cookiecutter-openedx/cookiecutter-openedx-devops.git"),
    install_requires=load_requirements("requirements/common.in"),
    zip_safe=False,
    keywords="Django, Open edX, Plugin",
    classifiers=[  # https://pypi.org/classifiers/
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
    ],
    entry_points={
        # mcdaniel feb-2022
        #
        # IMPORTANT: ensure that this entry_points coincides with that of edx-platform
        #            and also that you are not introducing any name collisions.
        # https://github.com/openedx/edx-platform/blob/master/setup.py#L88
        "lms.djangoapp": [
            "openedx_plugin = openedx_plugin.apps:CustomPluginConfig",
            "openedx_plugin_api = openedx_plugin_api.apps:CustomPluginAPIConfig",
            "openedx_plugin_mobile_api =" " openedx_plugin_mobile_api.apps:MobileApiConfig",
        ],
        "cms.djangoapp": [
            "openedx_plugin_cms = openedx_plugin_cms.apps:CustomPluginCMSConfig",
        ],
    },
    extras_require={
        "Django": ["Django>=3.2"],
    },
)
