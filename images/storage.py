"""Read and write the local files used by the image lab."""

import io
import os
from pathlib import Path


class LocalStore:
    def __init__(self, root=None):
        self.root = Path(
            root or os.getenv("STUDIO_STORE", Path(__file__).parent / "objects")
        ).resolve()

    def path(self, bucket, key):
        if (
            Path(bucket).name != bucket
            or ".." in Path(key).parts
            or Path(key).is_absolute()
        ):
            raise ValueError("Unsafe object path")
        result = (self.root / bucket / key).resolve()
        if self.root not in result.parents:
            raise ValueError("Object path escapes local store")
        return result

    def get_object(self, *, Bucket, Key):
        return {"Body": io.BytesIO(self.path(Bucket, Key).read_bytes())}

    def put_object(self, *, Bucket, Key, Body, ContentType=None):
        target = self.path(Bucket, Key)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(Body)
        return {"Key": Key}


def client():
    return LocalStore()
