import argparse
import importlib
import inspect
import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List, Optional


class StubEntry(ABC):
    def __init__(self, name: str, obj: Any, sub_modules: Optional[List["StubEntry"]] = None):
        self.obj = obj
        self.name = name
        self.children = sub_modules if sub_modules is not None else []

    @property
    def import_path(self) -> str:
        return f"{inspect.getmodule(self.obj).__name__}"

    def __repr__(self):
        return f"{self.name}"

    @abstractmethod
    def export(self, output_path: Path, intent: int = 0):
        pass

    def _create_string(self, lines: List[str], intent: int) -> str:
        lines.append("\n")
        spacing = " " * intent * 4
        lines = [f"{spacing}{l}" for l in lines]
        return "\n".join(lines)

    def _create_doc(self) -> List[str]:
        out = []
        doc = self.obj.__doc__

        if doc is not None and str(doc).strip() != "":
            out.append(f"    \"\"\"")
            out.append(f"    {self.obj.__doc__}")
            out.append(f"    \"\"\"")

        return out

    @property
    def has_children(self) -> bool:
        return len(self.children) > 0


class StubModule(StubEntry):

    def export(self, output_path: Path, intent: int = 0):
        print(f"exporting module {self.name}")

        if output_path.is_dir():
            os.makedirs(output_path, exist_ok=True)

        if self.has_sub_modules:
            output_path = output_path.joinpath(self.name)
            os.makedirs(output_path, exist_ok=True)

            module_path = output_path.joinpath("__init__.pyi")
        else:
            if output_path.is_file():
                output_path = output_path.parent

            module_path = output_path.joinpath(f"{self.name}.pyi")

        # create init file
        with open(module_path, "w"):
            pass

        for child in self.children:
            child.export(module_path)

    @property
    def has_sub_modules(self) -> bool:
        return len([child for child in self.children if isinstance(child, StubModule)]) > 0


class StubClass(StubEntry):
    def export(self, output_path: Path, intent: int = 0):
        out = []
        out.append(f"class {self.name}:")
        out += self._create_doc()

        if not self.has_children:
            out.append("    ...")

        with open(output_path, "a") as f:
            text = self._create_string(out, intent)
            f.writelines(text)

        for child in self.children:
            child.export(output_path, intent + 1)


class StubRoutine(StubEntry):
    def export(self, output_path: Path, intent: int = 0):
        out = []
        out.append(f"def {self.routine_signature()}:")
        out += self._create_doc()
        out.append(f"    ...")

        with open(output_path, "a") as f:
            text = self._create_string(out, intent)
            f.writelines(text)

    def __repr__(self):
        return f"{self.name}()"

    def routine_signature(self) -> str:
        return f"{self.name}(*args, **kwargs)"


class StubNanoBindFunction(StubRoutine):
    def __init__(self, name: str, obj: Any):
        super().__init__(name, obj)

        self.signature = self.parse_signature()

    def parse_signature(self) -> str:
        doc = self.obj.__doc__
        if doc is None:
            return super().routine_signature()

        doc_str = str(doc)
        parts = doc_str.split("\n")

        signature = parts[0]

        if not signature.startswith(self.name):
            return super().routine_signature()

        return signature

    def routine_signature(self) -> str:
        return self.signature


class NanobindStubsGenerator:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.module = importlib.import_module(self.module_name)

    def analyse(self) -> StubModule:
        result = self._analyse_module(self.module, StubModule(self.module_name, self.module))
        return result

    def _analyse_module(self, module, stub_entry: StubEntry) -> StubModule:
        for name, obj in inspect.getmembers(module):
            if name.startswith("_"):
                continue

            if inspect.isclass(obj):
                class_module = StubClass(name, obj)
                stub_entry.children.append(class_module)
                self._analyse_module(obj, class_module)

            if inspect.ismodule(obj):
                stub_module = StubModule(name, obj)
                stub_entry.children.append(stub_module)
                self._analyse_module(obj, stub_module)

            if inspect.isroutine(obj):
                stub_routine = StubRoutine(name, obj)
                stub_entry.children.append(stub_routine)

            if type(obj).__name__ == "nb_func":
                stub_nb_func = StubNanoBindFunction(name, obj)
                stub_entry.children.append(stub_nb_func)

        return stub_entry


def main():
    parser = argparse.ArgumentParser("Nanobind Stubs Generator")
    parser.add_argument("module", type=str, help="Module to create stubs for.")
    parser.add_argument("--output", type=str, default=".", help="Output path.")
    args = parser.parse_args()

    export_path = Path("../nanogui")
    if export_path.exists():
        shutil.rmtree(export_path)

    generator = NanobindStubsGenerator(args.module)
    stubs = generator.analyse()

    output_path = Path(args.output)
    stubs.export(output_path)


if __name__ == "__main__":
    main()
