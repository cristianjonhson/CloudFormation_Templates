from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


class CloudFormationLoader(yaml.SafeLoader):
    pass


def _construct_intrinsic(loader: CloudFormationLoader, tag_suffix: str, node: yaml.nodes.Node):
    tag_name = f"!{tag_suffix}"
    if isinstance(node, yaml.ScalarNode):
        value = loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        value = loader.construct_sequence(node)
    elif isinstance(node, yaml.MappingNode):
        value = loader.construct_mapping(node)
    else:
        raise TypeError(f"Nodo YAML no soportado para {tag_name}: {type(node)!r}")
    return {tag_name: value}


CloudFormationLoader.add_multi_constructor("!", _construct_intrinsic)


def discover_templates(root: Path) -> list[Path]:
    return sorted(path for path in root.glob("*.yaml") if path.is_file())


def validate_template(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            documents = list(yaml.load_all(handle, Loader=CloudFormationLoader))
        if not documents:
            return False, "el archivo no contiene documentos YAML"
        return True, f"{len(documents)} documento(s) YAML valido(s)"
    except yaml.YAMLError as error:
        return False, str(error)
    except OSError as error:
        return False, str(error)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida localmente la sintaxis YAML de templates CloudFormation."
    )
    parser.add_argument(
        "templates",
        nargs="*",
        help="Archivos .yaml concretos. Si no se indican, se validan todos los .yaml del directorio actual.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.templates:
        templates = [Path(template).resolve() for template in args.templates]
    else:
        templates = discover_templates(Path.cwd())

    if not templates:
        print("No se encontraron archivos .yaml para validar.", file=sys.stderr)
        return 1

    has_errors = False
    for template in templates:
        is_valid, message = validate_template(template)
        status = "OK" if is_valid else "ERROR"
        print(f"[{status}] {template.name}: {message}")
        has_errors = has_errors or not is_valid

    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
