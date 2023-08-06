import json
import yaml


def _is_valid_yaml_config_file(contents: str) -> bool:
    try:
        data = yaml.safe_load(contents)
        return data.get("glean") is not None
    except yaml.YAMLError:
        return False


def _is_valid_json_config_file(contents: str) -> bool:
    try:
        data = json.loads(contents)
        return data.get("glean") is not None
    except json.decoder.JSONDecodeError:
        return False


def is_valid_glean_config_file(filename: str, contents: str) -> bool:
    if filename.endswith(".yml") or filename.endswith(".yaml"):
        return _is_valid_yaml_config_file(contents)

    if filename.endswith(".json"):
        return _is_valid_json_config_file(contents)

    return False
