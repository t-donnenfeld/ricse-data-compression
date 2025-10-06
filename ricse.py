import hashlib
import os


def calculate_sha256(input_path: str) -> str:
    """Compute the sha256 hexadecimal summary of a file given its path."""
    hasher = hashlib.sha256()
    with open(input_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()


def compress_raw_with_jpeg(
    original_path: str, compressed_path: str, reconstructed_path: str, quality: int
) -> None:
    """Compress and decompress using JPEG classic and the enb library.
    :param original_path: Path to the raw file. Must have something like u8be-ZxYxX in its name
      so that geometry and data type can be inferred.
    :param compressed_path: Path to the output compressed file.
    :param reconstructed_path: Path to the reconstructed compressed file.
    :param quality: JPEG "quality" parameter (between 1 and 100)
    """
    assert os.path.exists(original_path)
    for path in (compressed_path, reconstructed_path):
        if os.path.exists(path):
            os.remove(path)
    assert quality == int(quality) and 1 <= int(
        quality) <= 100, f"Invalid {quality=}"

    # This part can be moved to the the top of your scripts
    import enb

    enb.plugins.install("jpeg")
    from ../../plugins/jpeg/jpeg_codecs import JPEG

    geometry_dict = enb.isets.file_path_to_geometry_dict(original_path)

    codec = JPEG(quality=quality)
    codec.compress(original_path, compressed_path, geometry_dict)
    codec.decompress(compressed_path, reconstructed_path, geometry_dict)


def compress_raw_with_jpeg_ls(
    original_path: str, compressed_path: str, reconstructed_path: str, max_error: int
) -> None:
    """Compress and decompress using JPEG classic and the enb library."""
    assert os.path.exists(original_path)
    for path in (compressed_path, reconstructed_path):
        if os.path.exists(path):
            os.remove(path)

    # This part can be moved to the the top of your scripts
    import enb

    enb.plugins.install("jpeg")
    from plugins.jpeg.jpeg_codecs import JPEG_LS

    geometry_dict = enb.isets.file_path_to_geometry_dict(original_path)

    codec = JPEG_LS(max_error=max_error)
    codec.compress(original_path, compressed_path, geometry_dict)
    codec.decompress(compressed_path, reconstructed_path, geometry_dict)


if __name__ == "__main__":
    print(
        "This is a python library. You can copy it into your project and import it with: `import ricse`"
    )
