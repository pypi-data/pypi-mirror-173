import base64

import numpy as np
from cv2 import cv2 as cv


def to_binary(frame: np.ndarray, extension: str = ".png") -> bytes:
    return cv.imencode(extension, frame)[1].tobytes()


def to_string(
    frame: np.ndarray, extension: str = ".png", encoding: str = "utf-8"
) -> str:
    return base64.b64encode(to_binary(frame=frame, extension=extension)).decode(
        encoding
    )


def from_binary(binary_image: bytes) -> np.ndarray:
    return cv.imdecode(np.frombuffer(binary_image, np.uint8), cv.IMREAD_UNCHANGED)


def from_string(encoded_image: str, encoding: str = "utf-8") -> np.ndarray:
    return from_binary(binary_image=base64.b64decode(encoded_image.encode(encoding)))
