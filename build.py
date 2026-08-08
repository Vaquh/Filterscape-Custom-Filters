import argparse
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
    parser = argparse.ArgumentParser()

    parser.add_argument("inputs", nargs="*")
    parser.add_argument("-o", "--output")

    args = parser.parse_args()

    metadata: FilterMetadata = load_filter_metadata()

    module_list: list[str] = []
    if args.inputs:
        module_list = args.inputs
    else:
        module_list = metadata["modules"]

    modules: list[Path] = []
    for module in module_list:
        module_path: Path = MODULE_DIR / module
        if module_path.is_dir():
            modules.append(module_path)

    header = build_header(metadata)
    body = build_body(modules)
    footer = build_footer()

    filter = join_non_empty([header, body, footer], "\n\n\n\n\n\n")
    filter += "\n"

    output_path: Path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path("vaquh_custom.rs2f")

    output_path.write_text(filter, encoding="utf-8", newline="\n")

if __name__ == "__main__":
    main()
