import pathlib
from io import BytesIO

import onnxruntime
from src.engines.background_removal.constants import ENV
from src.engines.background_removal.utils import (
    add_background,
    convert_image_to_bytes,
    get_foreground_image,
    get_mask,
    preprocess_image,
)
from src.engines.base.base_model import MLModel


class BackgroundRemoval(MLModel):
    @property
    def display_name(self):
        return "Remove Background Model"

    @property
    def checkpoint_dir(self):
        return pathlib.Path(__file__).parent / "checkpoints"

    @property
    def description(self):
        return (
            "A model predict a foreground of fashion image (remove background of image)"
        )

    @property
    def metadata(self):
        return {
            "MODEL_INPUT_SIZE": ENV.MODEL_INPUT_SIZE,
            "INPUT_TYPE": "BytesIO",
            "OUTPUT_TYPE": "BytesIO",
        }

    @property
    def model_instance(self):
        return "background_removal"

    def __init__(self):
        super().__init__(self)

        self.onnx_session = None
        self.checkpoint_path: str = self.checkpoint_dir / ENV.BR_MODEL_NAME
        self.load_checkpoint()

    @MLModel.update_checkpoint_status
    def load_checkpoint(self):
        self.onnx_session = onnxruntime.InferenceSession(
            self.checkpoint_path.as_posix()
        )

    def predict(self, image: BytesIO, background: BytesIO = None) -> BytesIO:
        try:
            origin_image, image_arr = preprocess_image(
                image, model_input_size=ENV.MODEL_INPUT_SIZE
            )
            model_input = {self.onnx_session.get_inputs()[0].name: image_arr}

            model_output = self.onnx_session.run(None, model_input)[0]
            model_output = model_output[:, 0, :, :]

            mask = get_mask(model_output, origin_image.size)
            foreground_image = get_foreground_image(mask, origin_image)

            if background:
                foreground_image = add_background(background, foreground_image)

            foreground_image = convert_image_to_bytes(foreground_image)

            return foreground_image
        except Exception as exc:
            import traceback

            print(traceback.format_exc())
            print(f"{self.display_name}: Error happen when predict, error due to {exc}")
            return None
