from src.engines.base.base_constants import Constants, get_env


class ENV(Constants):
    BR_MODEL_NAME = get_env("BR_MODEL_NAME", "background_removal.onnx")
    MODEL_INPUT_SIZE = (320, 320)
