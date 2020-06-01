import time

from fastapi import FastAPI
from starlette.requests import Request
from app.api.routes.router import api_router
from app.core.config import (API_PREFIX, APP_NAME, APP_VERSION, IS_DEBUG)

from app.core.event_handlers import (start_app_handler, stop_app_handler)


def get_app() -> FastAPI:
    rec_engine = FastAPI(title=APP_NAME, version=APP_VERSION, debug=IS_DEBUG)
    rec_engine.include_router(api_router, prefix=API_PREFIX)

    rec_engine.add_event_handler("startup", start_app_handler(rec_engine))
    rec_engine.add_event_handler("shutdown", stop_app_handler(rec_engine))

    return rec_engine


app = get_app()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
