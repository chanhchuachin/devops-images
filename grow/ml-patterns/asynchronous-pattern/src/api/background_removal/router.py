from celery.result import AsyncResult
from src.api.background_removal import tasks as br_tasks
from typing import Optional
from fastapi import APIRouter, HTTPException, Response
from src.engines.engine_registry import engine_manager
from fastapi.datastructures import UploadFile
from src.api.background_removal import models as br_models
from fastapi.param_functions import File
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from starlette import status
import binascii


br_router = APIRouter(prefix="/br", tags=["AI Models"])


def _to_task_out(result: AsyncResult) -> br_models.TaskOut:
    return br_models.TaskOut(task_id=result.id, status=result.status)


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


@br_router.post("/tasks", description="Create a prediction tasks!")
async def remove_background(
    file: UploadFile = File(...), file_bg: Optional[UploadFile] = File(None)
):
    model = engine_manager.get_model("background_removal")
    if model.checkpoint_status is True:
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File {file.filename} is not an image!",
            )
        else:
            file_content = binascii.b2a_base64(await file.read())

        bg_content = None
        if file_bg and file_bg.content_type.startswith("image/") is True:
            bg_content = binascii.b2a_base64(await file_bg.read())

        result = br_tasks.create_br_task.delay(file_content, bg_content)
        content = _to_task_out(result).json()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content={"task_id": content}
        )
    else:
        return f"Sorry! Engine: '{model.display_name}' haven't been load checkpoint!"


@br_router.get("/tasks/{task_id}", description="Get prediction results by task id!")
async def remove_background(task_id: str):
    task_result = AsyncResult(id=task_id)
    image_result = binascii.a2b_base64(task_result.result)
    task_result.forget()
    return Response(image_result, media_type="image/png")
