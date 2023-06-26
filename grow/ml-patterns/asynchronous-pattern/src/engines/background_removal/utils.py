from io import BytesIO
from typing import Tuple, Union

import numpy as np
from PIL import Image


def add_background(
    background_image: Union[BytesIO, Image.Image], foreground_image: Image.Image
) -> Image.Image:
    background_image = Image.open(background_image).convert("RGBA")
    foreground_image = foreground_image.resize(background_image.size)
    image_result = Image.alpha_composite(background_image, foreground_image)
    return image_result


def get_foreground_image(
    mask_image: Image.Image, origin_image: Image.Image
) -> Image.Image:
    mask_image_arr = np.array(mask_image)
    origin_image_arr = np.array(origin_image)
    br_arr = np.concatenate((origin_image_arr, mask_image_arr[:, :, [0]]), -1)
    br_image = Image.fromarray(br_arr.astype("uint8"), mode="RGBA")
    return br_image


def convert_image_to_bytes(image: Image.Image) -> BytesIO:
    br_image = BytesIO()
    image.save(br_image, "PNG")
    br_image.seek(0)
    return br_image


def normalize_prediction(d: np.array) -> np.array:
    ma = np.max(d)
    mi = np.min(d)
    dn = (d - mi) / (ma - mi)
    return dn


def get_mask(model_output: np.array, origin_image_size: Tuple[int, int]) -> Image.Image:
    mask = normalize_prediction(model_output).squeeze()
    mask = (
        Image.fromarray(mask * 255)
        .convert("RGB")
        .resize(origin_image_size, Image.LANCZOS)
    )
    return mask


def preprocess_image(image: BytesIO, model_input_size: Tuple[int, int]) -> np.array:
    origin_image = Image.open(image).convert("RGB")
    resize_image = origin_image.resize(model_input_size)
    image_arr = np.array(resize_image).astype(np.float32)
    image_arr = image_arr / np.max(image_arr)
    image_arr[:, :, 0] = (image_arr[:, :, 0] - 0.485) / 0.229
    image_arr[:, :, 1] = (image_arr[:, :, 1] - 0.456) / 0.224
    image_arr[:, :, 2] = (image_arr[:, :, 2] - 0.406) / 0.225

    image_arr = image_arr.transpose((2, 0, 1))
    image_arr = np.expand_dims(image_arr, axis=0)

    return origin_image, image_arr
