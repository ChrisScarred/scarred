from typing import Optional, Dict, List
from src.utils.parsing import nested_getter

class Translator:
    def __init__(self, sources: List[str]) -> None:
        self.sources = sources
        self.dict = {}
        self.is_loaded = False

    def get(self, var: str, def_val: Optional[str] = None) -> Optional[str]:
        return nested_getter(self.dict, var, def_val)

    def _load_dict(self) -> None:
        from yaml import load

        try:
            from yaml import CLoader as Loader
        except ImportError:
            from yaml import Loader
        
        for source in self.sources:
            with open(source, "r") as f:
                self.dict.update(load(f, Loader=Loader))
        self.is_loaded = True

    def translate(self, lang: str, key: str, default: Optional[str] = None, params: Dict = {}) -> str:
        if not self.is_loaded:
            self._load_dict()
        res = self.get(f"{lang}.{key}", default)
        if res:
            for k, v in params.items():
                res = res.replace(f"{{{k}}}", v)
        return res
        
