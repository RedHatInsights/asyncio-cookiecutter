from prometheus_client import Counter
from prometheus_client.exposition import choose_encoder, REGISTRY
from prometheus_async.aio import time  # noqa: F401
from aiohttp import web


counter = Counter("count", "Number of things that happened")


def _parse_content_type(content_type):
    if "charset" in content_type:
        parts = [p.strip() for p in content_type.split(";") if "charset" not in p]
        return "; ".join(parts)
    else:
        return content_type


async def metrics_handler(request):
    registry = REGISTRY
    encoder, content_type = choose_encoder(request.headers.get("Accept"))
    if "name[]" in request.query:
        registry = registry.restricted_registry(request.query["name[]"])
    try:
        return web.Response(
            content_type=_parse_content_type(content_type), body=encoder(registry)
        )
    except Exception:
        raise web.HTTPInternalServerError("error generating metric output")


def start():
    app = web.Application()
    app.add_routes([web.get("/metrics", metrics_handler)])
    web.run_app(app)
