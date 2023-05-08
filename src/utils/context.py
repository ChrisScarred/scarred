import os
from datetime import datetime
from typing import Any

from starlette.templating import Jinja2Templates

from src.utils.config import Config
from src.services.db_handler import Cockroach
from src.services.i18n import Translator
from src.utils.parsing import nested_getter


class Context:
    """Load, store, query, and add objects needed to be accessed during the lifetime of the application.

    Attributes:
        objects (Dict): the objects handled by this context handler, stored under their name in the dictionary.
    """
    def __init__(self, config: Config) -> None:
        """Initialise an instance of Context."""
        self.objects = {}
        self.config = config

    def get(self, var: str, def_val: Any = None) -> Any:
        return nested_getter(self.objects, var, def_val)

    def load_all(self) -> None:
        """Load the currently supperted objects.
        """
        self._locales()
        self._load_templates()
        self._load_db_conn()
    
    def _load_db_conn(self) -> None:
        """Load the database connection.
        """
        url = self.config.get("database_url")
        db = Cockroach(url)
        self.objects["cockroach"] = db
    
    def _locales(self) -> None:
        """Load locales and the translate function.
        """
        full_dir = os.path.join(self.config.get("base_dir"), self.config.get("app.resources.locales"))
        langs = [os.path.join(full_dir, x) for x in os.listdir(full_dir) if os.path.isfile(os.path.join(full_dir, x)) and ".yaml" in x]
        t = Translator(langs)
        t._load_dict()
        self.objects["locale"] = t.translate

    def _load_templates(self) -> None:
        """Obtain templates and register custom filter functions.
        """
        templates = Jinja2Templates(directory = self.config.get("app.resources.templates"))

        templates.env.filters["env_val"] = self.config.get
        templates.env.filters["year"] = lambda _: datetime.utcnow().year
        templates.env.filters["loc"] = self.get("locale")

        self.objects["templates"] = templates
