import re
from typing import Any, Optional
from functools import lru_cache

from src.utils.parsing import nested_getter

class ContextHandler:
    """Handle (load, store, query, and add) configuration variables.

    Attributes:
        conf_source (str): path to the configuration file.
        loaded (bool): flag indicating whether or not the configuration file was loaded.
        settings (Dict): the loaded settings from the configuation file.
    """
    def __init__(self, conf_source: str) -> None:
        """Initialise an instance of Config."""
        self.conf_source = conf_source
        self.loaded = False
        self.settings = {}
        self.db_regex = re.compile(r"\<([^\>]+)\>")

    def load_context(self, path: Optional[str] = None) -> None:
        """Load the configuration settings from the file."""
        from yaml import load

        try:
            from yaml import CLoader as Loader
        except ImportError:
            from yaml import Loader

        if path:
            with open(path, "r") as f:
                self.settings.update(load(f, Loader=Loader))

        else:
            with open(self.conf_source, "r") as f:
                self.settings.update(load(f, Loader=Loader))
            self.loaded = True

    def get(self, var: str, def_val: Any = None) -> Any:
        return nested_getter(self.settings, var, def_val)

    def add(self, key: str, val: Any) -> None:
        """Add a configuration variable `key` with a value `val`."""
        self.settings[key] = val
    
    def get_db_url(self) -> str:
        url_pattern = self.get("database.url_pattern")
        is_match = True
        while is_match:
            res = re.search(self.db_regex, url_pattern)
            if res:
                repl = res.group(1)
                url_pattern = url_pattern.replace(f"<{repl}>", self.get(repl, ""))
            else:
                is_match = False
        return url_pattern


@lru_cache
def load_context() -> ContextHandler:
    from dotenv import load_dotenv
    import os

    load_dotenv()
    src = os.getenv("APP_CONFIG_PATH")
    if src:
        context = ContextHandler(src)
        context.load_context()
        dname = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        context.add("base_dir", dname)
        return context

context = load_context()
