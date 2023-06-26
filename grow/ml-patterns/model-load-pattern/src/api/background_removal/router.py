import sys
from io import BytesIO
from typing import Optional
from fastapi import APIRouter, HTTPException, Response
from src.engines.engine_registry import engine_manager
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File
from fastapi.routing import APIRouter
from starlette import status


br_router = APIRouter(prefix="/br", tags=["AI Models"])


@br_router.get("/metadata", description="Metadata of background removal model!")
async def remove_background():
    result = [
        engine
        for engine in engine_manager.get_models()
        if engine.get("model_instance") == "background_removal"
    ]
    if result:
        return result[0]
    else:
        raise HTTPException(
            status_code=404, detail="Model is not define in Engine Manager!"
        )


@br_router.post("/predict", description="Predict foreground of image!")
async def remove_background(
    file: UploadFile = File(...),
    file_bg: Optional[UploadFile] = File(None),
):
    try:
        model = engine_manager.get_model("background_removal")

        if model.checkpoint_status is True:
            if not file.content_type.startswith("image/"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File {file.filename} is not an image.",
                )

            image_content = await file.read()

            bg_content = None
            if file_bg and file_bg.content_type.startswith("image/") is True:
                bg_content = BytesIO(await file_bg.read())

            rb_image: BytesIO = (
                engine_manager.get_model("background_removal")
                .predict(BytesIO(image_content), bg_content)
                .getvalue()
            )

            if rb_image is not None:
                return Response(rb_image, media_type="image/png")
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Sorry! {model.display_name} Can't predict background of image!",
                )
        else:
            return (
                f"Sorry! Engine: '{model.display_name}' haven't been load checkpoint!"
            )

    except Exception as exc:
        _, _, exc_tb = sys.exc_info()
        print(
            f"Error->routers->background_removal: %s - Line: %d"
            % (exc, exc_tb.tb_lineno),
        )
        return "INTERNAL_SERVER_ERROR"
