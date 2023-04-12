import logging
import os
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.services.context import ContextHandler
from src.services.i18n import Translator
from src.services.db_handler import Cockroach

class StartupManager:
    def __init__(self, context: ContextHandler) -> None:
        self.context = context

    def _load_templates(self) -> None:
        """Obtain templates and register custom filter functions.
        """
        templates = Jinja2Templates(directory = self.context.get("app.resources.templates"))
        templates.env.filters["env_val"] = self.context.get
        templates.env.filters["year"] = lambda _: datetime.utcnow().year
        templates.env.filters["loc"] = self.context.get("locale")
        self.context.add("templates", templates)

    def _mount_static(self) -> None:
        self.context.get("FastAPI").mount(
            f"/{self.context.get('routes.static')}",
            StaticFiles(directory=self.context.get("app.resources.static")),
            name=self.context.get("routes.static")
        )
    
    def _middleware(self) -> None:
        self.context.get("FastAPI").add_middleware(
            CORSMiddleware,
            allow_origins=self.context.get("security.origins"),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logging.debug(f"CORSMiddleware allowed origins are `{self.context.get('security.origins')}`.")
        
        self.context.get("FastAPI").add_middleware(TrustedHostMiddleware, allowed_hosts=self.context.get("security.hosts"))
        logging.debug(f"TrustedHostMiddleware allowed hosts are `{self.context.get('security.hosts')}`.")

        self.context.get("FastAPI").add_middleware(HTTPSRedirectMiddleware)

    def _locales(self) -> None:
        full_dir = os.path.join(self.context.get("base_dir"), self.context.get("app.resources.locales"))
        langs = [os.path.join(full_dir, x) for x in os.listdir(full_dir) if os.path.isfile(os.path.join(full_dir, x)) and ".yaml" in x]
        t = Translator(langs)
        t._load_dict()
        self.context.add("locale", t.translate)

    def _load_routes(self) -> None:
        route_path = self.context.get("app.resources.routes")
        abs_route_path = os.path.join(self.context.get("base_dir"), route_path)
        self.context.load_context(path=abs_route_path)

    def _init_db(self) -> None:
        url = self.context.get_db_url()
        db = Cockroach(url)
        self.context.add("Cockroach", db)

    def start_up(self) -> None:
        self._middleware()
        self._locales()
        self._load_routes()
        self._mount_static()
        self._load_templates()
        self._init_db()
