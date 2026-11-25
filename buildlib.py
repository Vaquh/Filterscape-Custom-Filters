import json
from pathlib import Path
from typing import cast, NotRequired, TypedDict

from paths import TEMPLATE_DIR

class ModuleConfig(TypedDict):
    order: NotRequired[list[str]]

class FilterMetadata(TypedDict):
    name: str
    description: str
    modules: list[str]

def normalize_string(string: str) -> str:
    string = string.replace("\r\n", "\n")
    string = string.replace("\r", "\n")
    string = string.lstrip("\n")
    string = string.rstrip()

    return string

def join_non_empty(strings: list[str], separator: str) -> str:
    non_empty_strings: list[str] = []

    for string in strings:
        if string.strip():
            non_empty_strings.append(string)

    return separator.join(non_empty_strings)

def load_section(filepath: Path) -> str:
    text: str = filepath.read_text(encoding="utf-8")

    return normalize_string(text)

def build_module(module_path: Path) -> str:
    config: ModuleConfig = {}
    config_path: Path = module_path / "module.json"

    if config_path.is_file():
        config = cast(ModuleConfig, json.loads(config_path.read_text(encoding="utf-8")))

    module_section_paths: list[Path] = []

    for section_name in config.get("order", []):
        section_path: Path = module_path / f"{section_name}.rs2f"
        if section_path.is_file():
            module_section_paths.append(section_path)

    discovered_section_paths: list[Path] = sorted(module_path.glob("*.rs2f"))

    for section_path in discovered_section_paths:
        if section_path not in module_section_paths:
            module_section_paths.append(section_path)

    module_sections: list[str] = []

    for section_path in module_section_paths:
        module_sections.append(load_section(section_path))


    module: str = join_non_empty(module_sections, "\n\n")

    return module

def build_body(module_paths: list[Path]) -> str:
    modules: list[str] = []

    for module_path in module_paths:
        if module_path.is_dir():
            modules.append(build_module(module_path))

    body: str = join_non_empty(modules, "\n\n\n\n")

    return body

def build_footer() -> str:
    footer: str = ""
    footer_path: Path = TEMPLATE_DIR / "footer.json"

    if footer_path.is_file():
        footer = footer_path.read_text(encoding="utf-8")

    return normalize_string(footer)

def build_header(metadata: FilterMetadata) -> str:
    header: str = ""
    header_path: Path = TEMPLATE_DIR / "header.rs2f"

    if header_path.is_file():
        header = header_path.read_text(encoding="utf-8")

    header = header.replace("{name}", metadata["name"])
    header = header.replace("{description}", metadata["description"])

    return normalize_string(header)
