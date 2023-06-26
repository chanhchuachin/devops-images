import sys
import src.engines.base.gdrive_helper as gdrive_helper
from src.api.engine import models as engine_models
from src.engines.engine_registry import engine_manager
from fastapi import Body, HTTPException
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse, Response
from starlette import status


engine_router = APIRouter(prefix="/engine", tags=["engines"])


@engine_router.get("")
async def get_engines():
    return engine_manager.get_models()


@engine_router.post("/reload")
async def reload_engine(
    engine: engine_models.BaseEngine,
):
    try:
        class_path = engine_manager.get_model(engine.model_instance).class_path
        engine_manager.remove_model(engine.model_instance)
        engine_manager.load_model(class_path)
        return "Reload Engine Successfully!"
    except:
        raise HTTPException(
            detail="Model instance not found!", status_code=status.HTTP_404_NOT_FOUND
        )


@engine_router.post("/update_models")
async def update_checkpoints(
    engine_list: list[engine_models.Engine],
):
    try:
        gdrive_client = gdrive_helper.GoogleDriveHelper()
        final_version = {}

        for request_engine in engine_list:
            print(request_engine)
            try:
                engine = engine_manager.get_model(request_engine.model_instance)
            except:
                final_version[
                    request_engine.model_instance
                ] = "Can't find engine name in engine_manager!"
                continue

            if (
                request_engine.checkpoint_version == engine.checkpoint_version
                and engine.checkpoint_status is True
            ):
                final_version[
                    request_engine.model_instance
                ] = f"Current version model is latest!"
                continue

            if not engine.checkpoint_dir.exists():
                engine.checkpoint_dir.mkdir(parents=True, exist_ok=True)

            status = True
            for model_file in request_engine.files:
                file_name, gdriver_id = model_file.name, model_file.gdriver_id

                print(file_name, gdriver_id)
                output_file = engine.checkpoint_dir / file_name
                status = gdrive_client.download_file(gdriver_id, output_file)

                if status is False:
                    break

                if status:
                    # reload model and update new model_version
                    engine.load_checkpoint()
                    engine.checkpoint_version = request_engine.checkpoint_version
                    final_version[
                        request_engine.model_instance
                    ] = engine.checkpoint_version

                else:
                    # download file failed!
                    final_version[
                        request_engine.model_instance
                    ] = "Error happen when download file, please check google drive id of each file!"

        return JSONResponse(final_version)
    except Exception as exc:
        _, _, exc_tb = sys.exc_info()
        print(
            "Error->routers->update_checkpoints: %s - Line: %d"
            % (exc, exc_tb.tb_lineno)
        )
        return "INTERNAL_SERVER_ERROR"
