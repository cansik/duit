from pathlib import Path
from typing import List

from setuptools import setup, find_packages

required_packages = find_packages(exclude=["test", "examples"])

BASE_NAME = "__required__"
ALL_NAME = "all"


def parse_requirements():
    extras = {}

    with open('requirements.txt') as f:
        lines = f.read().splitlines()

    extra_name = BASE_NAME
    extra_items: List[str] = []

    for line in [line.strip() for line in lines if line != ""]:
        if line.startswith("# extra"):
            extras[extra_name] = extra_items
            extra_items: List[str] = []

            tokens = line.split(" ")
            extra_name = tokens[2]

        elif line.startswith("#"):
            pass
        elif line.startswith("-"):
            pass
        else:
            extra_items.append(line)

    # add last group
    extras[extra_name] = extra_items

    # extract base packages
    install = extras.pop(BASE_NAME)

    # create all group
    all_reqs = list(extras.values())
    extras[ALL_NAME] = []
    for reqs in all_reqs:
        extras[ALL_NAME] += reqs

    return install, extras


install_required, extras_required = parse_requirements()

# read readme
current_dir = Path(__file__).parent
long_description = (current_dir / "README.md").read_text()

setup(
    name="simbi",
    version='0.1.2',
    packages=required_packages,
    url='https://github.com/cansik/simbi',
    license='MIT License',
    author='Florian Bruggisser',
    author_email='github@broox.ch',
    description='Simbi is a toolkit to create simple user-interfaces for python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_required,
    extras_require=extras_required
)
