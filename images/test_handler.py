import io
import json
import sys
import unittest
from unittest.mock import patch, MagicMock
from PIL import Image, UnidentifiedImageError
from handler import handler, resize_image


def image_bytes(size=(500, 400)):
    stream = io.BytesIO()
    Image.new("RGB", size, (20, 100, 180)).save(stream, format="PNG")
    return stream.getvalue()


def event(key="uploads/sample.png"):
    return {
        "Records": [
            {"s3": {"bucket": {"name": "frontier-media"}, "object": {"key": key}}}
        ]
    }


class ImageTests(unittest.TestCase):
    def test_resize_dimensions_and_format(self):
        for size in [(500, 400), (100, 400), (40, 40)]:
            result = Image.open(io.BytesIO(resize_image(image_bytes(size))))
            self.assertEqual(result.format, "PNG")
            self.assertLessEqual(max(result.size), 128)
            self.assertAlmostEqual(
                result.width / result.height, size[0] / size[1], delta=0.04
            )

    def test_invalid_raises_pillow_error(self):
        with self.assertRaises(UnidentifiedImageError):
            resize_image(b"invalid")

    def test_handler_downloads_decoded_key_and_stores_png(self):
        store = MagicMock()
        store.get_object.return_value = {"Body": io.BytesIO(image_bytes())}
        with patch("handler.storage.client", return_value=store):
            response = handler(event("uploads/a+b.png"), None)
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"])["token"], "SCALE_OK")
        store.get_object.assert_called_once_with(
            Bucket="frontier-media", Key="uploads/a b.png"
        )
        saved_object = store.put_object.call_args.kwargs
        self.assertEqual(saved_object["Key"], "thumbnails/uploads/a b.png.png")
        self.assertEqual(saved_object["ContentType"], "image/png")
        self.assertLessEqual(
            max(Image.open(io.BytesIO(saved_object["Body"])).size), 128
        )

    def test_invalid_image_does_not_upload(self):
        store = MagicMock()
        store.get_object.return_value = {"Body": io.BytesIO(b"bad")}
        with patch("handler.storage.client", return_value=store):
            response = handler(event(), None)
        self.assertNotEqual(response["statusCode"], 200)
        store.put_object.assert_not_called()

    def test_output_event_is_ignored(self):
        store = MagicMock()
        with patch("handler.storage.client", return_value=store):
            response = handler(event("thumbnails/uploads/sample.png.png"), None)
        store.get_object.assert_not_called()
        store.put_object.assert_not_called()
        self.assertNotIn("SCALE_OK", json.dumps(response))

    def test_duplicate_delivery_uses_same_output_key(self):
        store = MagicMock()
        store.get_object.side_effect = lambda **kw: {"Body": io.BytesIO(image_bytes())}
        with patch("handler.storage.client", return_value=store):
            handler(event(), None)
            handler(event(), None)
        self.assertEqual(
            [x.kwargs["Key"] for x in store.put_object.call_args_list],
            ["thumbnails/uploads/sample.png.png"] * 2,
        )

    def test_multiple_records(self):
        store = MagicMock()
        store.get_object.side_effect = lambda **kw: {"Body": io.BytesIO(image_bytes())}
        upload_event = event()
        upload_event["Records"] += event("uploads/second.png")["Records"]
        with patch("handler.storage.client", return_value=store):
            handler(upload_event, None)
        self.assertEqual(store.put_object.call_count, 2)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ImageTests)
    )
    if result.wasSuccessful():
        print(
            "IMAGE_LOGIC_OK: mocked storage checks only; local HTTP event delivery still required"
        )
    sys.exit(not result.wasSuccessful())
