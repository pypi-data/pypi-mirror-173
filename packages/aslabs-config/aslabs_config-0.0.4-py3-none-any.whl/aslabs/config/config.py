from dataclasses import Field, fields, is_dataclass, _MISSING_TYPE
import os
import json
from typing import Any, TypeVar, get_type_hints
from dotenv import dotenv_values

T = TypeVar("T")


class Config:
    def __init__(self):
        self._full_config = {}

    def _add_config_merged(self, data: dict[str, Any]):
        def merge(source: dict, dest: dict):
            for key, value in source.items():
                if isinstance(value, dict):
                    node = dest.setdefault(key.lower(), {})
                    merge(value, node)
                else:
                    dest[key.lower()] = value
            return dest

        self._full_config = merge(data, self._full_config)

    def add_dict(self, conf: dict[str, Any]) -> "Config":
        self._add_config_merged(conf)
        return self

    def add_file(self, path: str) -> "Config":
        if not os.path.isfile(path):
            return self
        try:
            with open(path) as f:
                data = json.load(f)
            self._add_config_merged(data)
        except json.JSONDecodeError:
            return self
        return self

    def _parse_flat_env_vars(self, vars: dict[str, str]) -> dict:
        nested = {}

        for key, value in vars.items():
            d = nested
            *nesting, final = key.split("__")
            for k in nesting:
                if k not in d:
                    d[k] = {}
                d = d[k]
            d[final] = value
        return nested


    def add_env_variables(self, prefix: str) -> "Config":
        data = {
            key[len(prefix):]: value
            for key, value in os.environ.items()
            if key.startswith(prefix)}

        nested = self._parse_flat_env_vars(data)

        self._add_config_merged(nested)
        return self

    def add_dotenv(self, file=".env"):
        data = dotenv_values(file)

        nested = self._parse_flat_env_vars(data)

        self._add_config_merged(nested)
        return self

    def resolve(self, config_cls: type[T], section: str = None) -> T:
        assert is_dataclass(config_cls), f"Expected data class, got {config_cls}"
        conf_dict = self._full_config
        if section is not None:
            sections = section.split(":")
            for section in sections:
                if section in conf_dict:
                    conf_dict = conf_dict[section]
                else:
                    break

        def _get_default(field: Field):
            if not isinstance(field.default_factory, _MISSING_TYPE):
                return field.default_factory()
            if not isinstance(field.default, _MISSING_TYPE):
                return field.default
            return None

        full_types = get_type_hints(config_cls)

        def _resolve_type(field: Field):
            _type = field.type
            if isinstance(field.type, str):
                _type = full_types[field.name]
            return _type

        return config_cls(
            **{
                field.name: _resolve_type(field)(conf_dict.get(field.name))
                if field.name in conf_dict else _get_default(field)
                for field in fields(config_cls)
            }
        )
