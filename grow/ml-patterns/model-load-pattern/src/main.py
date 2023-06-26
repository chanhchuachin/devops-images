from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import api_router
from src.core.config import settings


app = FastAPI(title=settings.TITLE, root_path=settings.ROOT_PATH)


@app.get(app.root_path + "/openapi.json", include_in_schema=False)
def custom_swagger_ui_html():
    return app.openapi()


# need to modify here
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(api_router, prefix=settings.ROOT_PATH)
