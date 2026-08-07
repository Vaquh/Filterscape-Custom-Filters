import json
from pathlib import Path
from typing import cast

from builder import FilterMetadata, build_header, build_body, build_footer, join_non_empty
from paths import FILTER_PATH, MODULE_DIR

def load_filter_metadata() -> FilterMetadata:
    if not FILTER_PATH.is_file():
        raise FileNotFoundError(FILTER_PATH)

    return cast(FilterMetadata, json.loads(FILTER_PATH.read_text(encoding="utf-8")))

def main():
    metadata: FilterMetadata = load_filter_metadata()

    modules: list[Path] = []
    for module in metadata["modules"]:
        module_path: Path = MODULE_DIR / module
        if module_path.is_dir():
            modules.append(module_path)

    header = build_header(metadata)
    body = build_body(modules)
    footer = build_footer()

    filter = join_non_empty([header, body, footer], "\n\n\n\n\n\n")
    filter += "\n"

    _ = Path("vaquh_custom.rs2f").write_text(filter, encoding="utf-8", newline="\n")

if __name__ == "__main__":
    main()
