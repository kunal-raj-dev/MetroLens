import io
import struct

import pytest
from PIL import Image, PngImagePlugin

from apps.api.errors import DecompressionBombError
from apps.api.middleware.security import ImageSecurityValidator


def test_orientation_reports_dimensions_of_returned_image():
    image = Image.new("RGB", (1200, 800), "gray")
    exif = Image.Exif()
    exif[274] = 6
    exif[315] = "private creator"
    source = io.BytesIO()
    image.save(source, format="JPEG", exif=exif)
    record = ImageSecurityValidator.sanitize_and_verify(source.getvalue())
    decoded = Image.open(io.BytesIO(record.sanitized_bytes))
    assert (record.width, record.height) == decoded.size == (800, 1200)
    assert not decoded.getexif()


def test_png_exif_is_removed_not_implicitly_resaved():
    image = Image.new("RGB", (800, 600), "gray")
    exif = Image.Exif()
    exif[315] = "private creator"
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("location", "private location")
    source = io.BytesIO()
    image.save(source, format="PNG", exif=exif, pnginfo=metadata)
    record = ImageSecurityValidator.sanitize_and_verify(source.getvalue())
    decoded = Image.open(io.BytesIO(record.sanitized_bytes))
    assert not decoded.getexif()
    assert "location" not in decoded.info


@pytest.mark.parametrize("width,height", [(9000, 600), (8000, 6000)])
def test_dimension_limits_reject_before_raster_decode(width, height):
    # Header only: no allocation of an oversized raster is necessary.
    data = b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", width, height)
    with pytest.raises(DecompressionBombError) as error:
        ImageSecurityValidator.sanitize_and_verify(data)
    assert error.value.details["max_pixels"] == 40_000_000
    assert error.value.details["max_dimension"] == 8000
    assert "40 megapixels" in error.value.message
    assert "8000 pixels per side" in error.value.message
    assert "64" not in error.value.remediation


def test_minimum_resolution_uses_oriented_dimensions():
    import io
    from PIL import Image
    from apps.api.middleware.security import ImageSecurityValidator
    image = Image.new("RGB", (600, 800), "gray")
    exif = Image.Exif()
    exif[274] = 6
    payload = io.BytesIO()
    image.save(payload, format="JPEG", exif=exif)
    record = ImageSecurityValidator.sanitize_and_verify(payload.getvalue())
    assert (record.width, record.height) == (800, 600)
