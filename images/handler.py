"""Complete these two functions for Lab 12."""

import io
import json
from urllib.parse import unquote_plus

import storage
from PIL import Image, UnidentifiedImageError

THUMBNAIL_SIZE = (128, 128)


def resize_image(image_bytes):
    # Open the image, keep its proportions and return PNG bytes.
    # The result must fit inside THUMBNAIL_SIZE.
    raise NotImplementedError("Implement resize_image")


def handler(event, context):
    # Work through every record in event["Records"].
    # Skip thumbnail events, then decode the input key and read the image.
    # Resize it and save thumbnails/<original-key>.png with image/png.
    # Return SCALE_OK only after saving. Invalid images must not be written.
    raise NotImplementedError("Implement handler")
