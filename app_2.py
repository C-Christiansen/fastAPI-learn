from fastapi import FastAPI, Depends
from .dependencies import RequiresScope, RequiresActor
from .fake_data import FakeGetMeteringPointList, FakeToken


def create_app() -> FastAPI:
    """Create a new instance of the application."""

    app = FastAPI(
        title='MeteringPoints API',
    )

    @app.get("/")
    async def root():
        return {"message": "http://localhost:8000/docs,"
                           "http://localhost:8000/list, "
                           "http://localhost:8000/token"
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
            Depends(RequiresScope(
                scope='meteringpoints.read'
            )),
            Depends(RequiresActor(
                actor='foo'
            )),
        ],
    )

    return app
