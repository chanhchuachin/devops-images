import binascii
from io import BytesIO
from src.core.worker import celery
from src.engines.engine_registry import engine_manager

@celery.task
def create_br_task(image_content, bg_content):
    image_content = binascii.a2b_base64(image_content)
    if bg_content:
        bg_content = binascii.a2b_base64(bg_content)

    rb_image: BytesIO = engine_manager.get_model("background_removal").predict(BytesIO(image_content), bg_content).getvalue()
    return binascii.b2a_base64(rb_image)
