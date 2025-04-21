from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from backend.api.main import api_router


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title='TheHive',
    openapi_url="/api/v1/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix='/api/v1')

if __name__ == "__main__":
    uvicorn.run('backend.app:app', reload=True)