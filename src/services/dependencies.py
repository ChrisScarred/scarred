import os
from functools import lru_cache

from dotenv import load_dotenv

from src.services.config import Config
from src.services.context import Context


@lru_cache
def load_config() -> Config:
    """Load config. Cached so that it can be re-imported with minumum performance impact.
    """
    load_dotenv()
    src = os.getenv("APP_CONFIG_PATH")
    config = Config(src)
    config.load_config()
    dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    config.add("base_dir", dir_name)
    config.get_db_url()
    return config

@lru_cache
def load_routes(config: Config) -> Config:
    route_path = config.get("app.resources.routes")
    abs_route_path = os.path.join(config.get("base_dir"), route_path)
    routes = Config(abs_route_path)
    routes.load_config()
    return routes

@lru_cache
def load_context(config: Config) -> Context:
    """Upon the first call of this function, load the following context objects:
        templates (starlette.templating.Jinja2Templates): the Jinja 2 templates.
        loacale (src.services.i18n.Translator:translate): the translation function.
        cockroach (src.services.db_handler.Cockroach): the cockroach database handler
    """
    context = Context(config)
    context.load_all()
    return context

config = load_config()
routes = load_routes(config)
context = load_context(config)