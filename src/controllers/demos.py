from starlette.requests import Request

from src.services.context import ContextHandler

def router(request: Request, context: ContextHandler):
    params = request.query_params
    if len(params.keys()) == 0:
        return overview(request, context)
    return demo(request, context)

def overview(request: Request, context: ContextHandler):
    return context.get("Cockroach").test()

def demo(request: Request, context: ContextHandler):
    pass
