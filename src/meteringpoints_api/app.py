from dataclasses import field
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, Cookie, HTTPException
from .dependencies import RequiresScope, RequiresActor
from .fake_data import FakeGetMeteringPointList, FakeToken


def query_extractor(cookie: Optional[str] = None):
    return cookie


def query_or_cookie_extractor(
        q: str = Depends(
            RequiresActor(actor='foo')),
        cookie: Optional[str] = Cookie(None)
):
    if q:
        print('cookie')
   # else:
    #    raise HTTPException(status_code=404, detail="Item not found")


def create_app() -> FastAPI:
    """Create a new instance of the application."""

    app = FastAPI(
        title='MeteringPoints API',
    )

    @app.get("/")
    async def root():
        return {"message": "http://localhost:8000/docs, "
                           "http://localhost:8000/list, "
                           "http://localhost:8000/token "
                }

    app.add_api_route(
        path='/token',
        methods=['POST'],
        endpoint=FakeToken().handle_request,
    )

    app.add_api_route(
        path='/list',
        methods=['GET'],
        endpoint=FakeGetMeteringPointList().handle_request,
        dependencies=[
            Depends(query_or_cookie_extractor),
        ],
    )

    @app.post("/cookie/")
    def create_cookie():
        content = {"message": "Come to the dark side, we have cookies"}
        response = JSONResponse(content=content)
        response.set_cookie(key="fakesession",
                            value="foo")
        return response

    return app
