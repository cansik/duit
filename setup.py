import distutils
from distutils.command.install import install
from pathlib import Path
from typing import List

from setuptools import setup, find_packages

PACKAGE_NAME = "duit"
PACKAGE_VERSION = "0.1.18.1"
PACKAGE_URL = "https://github.com/cansik/duit"

PACKAGE_DOC_MODULES = ["duit", "!duit.vision"]

required_packages = find_packages(exclude=["tests", "examples", "scripts", "playground"])

BASE_NAME = "__required__"
ALL_NAME = "all"


def parse_requirements():
    extras = {}

    with open("requirements.txt") as f:
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


class GenerateDoc(distutils.cmd.Command):
    description = "generate pdoc documentation"

    user_options = install.user_options + [
        ("output=", None, "Output path for the documentation."),
        ("launch", None, "Launch webserver to display documentation.")
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.output: str = "docs"
        self.launch: bool = False

    def finalize_options(self):
        pass

    def run(self) -> None:
        from scripts.generate_doc import generate_doc
        generate_doc(PACKAGE_NAME, PACKAGE_VERSION, PACKAGE_URL, required_packages,
                     Path(self.output), PACKAGE_DOC_MODULES, launch=bool(self.launch))


# read readme
current_dir = Path(__file__).parent
long_description = (current_dir / "README.md").read_text()

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    packages=required_packages,
    url=PACKAGE_URL,
    license="MIT License",
    author="Florian Bruggisser",
    author_email="github@broox.ch",
    description="Duit is a toolkit to create simple user-interfaces for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_required,
    extras_require=extras_required,
    cmdclass={
        "doc": GenerateDoc,
    },
)
