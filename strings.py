import json
import logging
from typing import Dict, Self, Any

import paths


class ObStrings:
    _instance: Self = None
    _strings_dict: Dict[str, str] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            with open(paths.STRINGS_FILE) as fp:
                cls._strings_dict = json.load(fp)
        return cls._instance

    def __getattr__(self, name) -> 'ObStrings.Formatter':
        if name in self._strings_dict:
            return ObStrings.Formatter(self._strings_dict[name])
        logging.error(f"String '{name}' not found!")
        return ObStrings.ErrorFormatter(name)

    class Formatter:
        def __init__(self, string: str):
            self.__string = string

        def __call__(self, *args: Any) -> str:
            try:
                return self.__string.format(*args)
            except Exception as e:
                return ObStrings._strings_dict.get("ERROR_FORMATTING", "ERROR WHEN FORMATTING: {0}").format(e)

    class ErrorFormatter(Formatter):
        def __init__(self, error_key: str):
            super().__init__(
                ObStrings._strings_dict.get("ERROR_NOT_FOUND", "ERROR: MISSING STRING {0}").format(error_key)
            )

        def __call__(self, *args: Any) -> str:
            return super().__call__()