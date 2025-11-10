from collections import Counter
from typing import Literal, Union

import numpy as np
from numpy.typing import NDArray

from entropy_coders import ricse
from .quant import quantize_midrise_mid


class RawImage:
    data: Union[
        NDArray[np.generic],
        NDArray[np.uint8],
        NDArray[np.uint16],
        NDArray[np.int8],
        NDArray[np.int16],
    ]

    def __init__(
        self,
        path: str,
        width: int,
        height: int,
        channel_nbr: int,
        sample_size: int = 1,
        signed: bool = False,
        endianness: Literal["little", "big"] = "big",
        ordering: Literal["BSQ", "BIP", "BIL"] = "BSQ",
    ):
        self.path = path
        self.width = width
        self.height = height
        self.channel_nbr = channel_nbr
        self.sample_size = sample_size
        self.signed = signed
        self.endianness = endianness
        self.ordering = ordering

        dtype_str = "<" if endianness == "little" else ">"
        dtype_str += {
            1: "i1" if signed else "u1",
            2: "i2" if signed else "u2",
            4: "i4" if signed else "u4",
        }[sample_size]
        self.dtype = np.dtype(dtype_str)

        raw = np.fromfile(path, dtype=self.dtype)
        if ordering == "BSQ":
            self.data = raw.reshape((channel_nbr, height, width))
        elif ordering == "BIP":
            self.data = raw.reshape((height, width, channel_nbr))
        else:
            self.data = np.zeros((height, width))
            raise NotImplementedError("BIL ordering not yet supported")

    def __copy__(self):
        cls = self.__class__
        new = cls.__new__(cls)

        new.path = self.path
        new.width = self.width
        new.height = self.height
        new.channel_nbr = self.channel_nbr
        new.sample_size = self.sample_size
        new.signed = self.signed
        new.endianness = self.endianness
        new.ordering = self.ordering
        new.dtype = self.dtype

        # depp copy to avoid sharing data
        new.data = self.data.copy()

        return new

    def get_value(self, x, y, channel):
        if self.ordering == "BSQ":
            return self.data[channel, y, x]
        else:  # BIP
            return self.data[y, x, channel]

    def set_value(self, x, y, channel, value):
        if self.ordering == "BSQ":
            self.data[channel, y, x] = value
        else:
            self.data[y, x, channel] = value

    def get_pixel(self, x, y):
        if self.ordering == "BSQ":
            return self.data[:, y, x]
        else:
            return self.data[y, x, :]

    def to_BIP(self):
        if self.ordering == "BIP":
            return
        self.data = np.moveaxis(self.data, 0, -1)
        self.ordering = "BIP"

    def to_higher_sample_size(
        self, new_sample_size: int, byteorder: Literal["little", "big"]
    ):
        if new_sample_size <= self.sample_size:
            return
        new_dtype_str = ("<" if byteorder == "little" else ">") + {2: "u2", 4: "u4"}[
            new_sample_size
        ]
        self.data = self.data.astype(new_dtype_str)
        self.sample_size = new_sample_size
        self.endianness = byteorder

    def count_true_bits(self):
        arr = self.data.view(np.uint8)
        bits = np.unpackbits(arr)
        return bits.sum()

    def set_green_msbs_to_one(self):
        if self.channel_nbr < 2:
            return
        self.data[1] = self.data[1] | 0b10000000

    def set_blue_lsbs_to_zero(self):
        if self.channel_nbr < 3:
            return
        self.data[2] = self.data[2] & 0b11111110

    def get_bytes_histogram_of_channel(self, channel):
        values, counts = np.unique(self.data[channel].ravel(), return_counts=True)
        return dict(zip(values.tolist(), counts.tolist()))

    def get_bytes_histogram(self):
        combined = Counter()
        for c in range(self.channel_nbr):
            combined += Counter(self.get_bytes_histogram_of_channel(c))
        return dict(combined)

    def write(self, path):
        self.data.astype(self.dtype).tofile(path)

    def get_jpeg_compressed(self):
        return ricse.compress_raw_with_jpeg(
            self.path, "./compressed.jpg", "reconstructed.jpg", 1
        )

    def add_ppm_header(self, header_path: str) -> None:
        with open(header_path, "rb") as f:
            header = f.read()
        data_bytes = self.data.astype(self.dtype).tobytes(order="C")
        combined = header + data_bytes
        self._with_header = combined

    def get_bitplane_component(
            self,
            bit: int,
    ) -> NDArray[np.uint8]:
        arr = self.data.astype(np.uint8)
        return ((arr >> bit) & 1).astype(np.uint8)

    def write_black_and_white_bitplane_component(
            self,
            bit: int,
            path: str,
    ) -> None:
        arr = self.get_bitplane_component(bit)
        arr = arr * 0xFF
        arr.tofile(path)

    def get_copy_quantized(self, step):
        new = self.__copy__()
        new.data = quantize_midrise_mid(self.data, step)
        return new
