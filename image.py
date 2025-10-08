import ricse
from collections import Counter


class RawImage:
    def __init__(
        self, path, width, height, channel_nbr, data_type="u8be", ordering="BSQ"
    ) -> None:
        self.width = width
        self.path = path
        with open(path, "rb") as f:
            self.data = bytearray(f.read())
        self.height = height
        self.channel_nbr = channel_nbr
        self.data_type = data_type
        self.ordering = ordering

    def set_value(self, x, y, channel, value):
        if self.ordering == "BSQ":
            self.set_value_bsq(x, y, channel, value)
        if self.ordering == "BIL":
            # TODO
            self.set_value_bsq(x, y, channel, value)
        else:
            self.set_value_bip(x, y, channel, value)

    def get_value(self, x, y, channel):
        if self.ordering == "BSQ":
            return self.get_value_bsq(x, y, channel)
        if self.ordering == "BIL":
            # TODO
            return self.get_value_bsq(x, y, channel)
        else:
            return self.get_value_bip(x, y, channel)

    def set_value_bsq(self, x, y, channel, value):
        offset = (y * self.width + x) + channel * self.width * self.height
        self.data[offset] = value

    def get_value_bsq(self, x, y, channel):
        offset = (y * self.width + x) + channel * self.width * self.height
        return self.data[offset]

    def set_value_bip(self, x, y, channel, value):
        offset = y * self.width * self.channel_nbr + x * self.channel_nbr * channel
        self.data[offset] = value

    def get_value_bip(self, x, y, channel):
        offset = y * self.width * self.channel_nbr + x * self.channel_nbr * channel
        return self.data[offset]

    def get_pixel(self, x, y):
        return [self.get_value(x, y, i) for i in range(self.channel_nbr)]

    def to_BIP(self):
        new = bytearray()
        for y in range(self.height):
            for x in range(self.width):
                for pixel_component in self.get_pixel(x, y):
                    new.append(pixel_component)
        self.data = new
        self.ordering = "BIP"

    def count_true_bits(self):
        sum = 0
        for byte in self.data:
            for i in range(8):
                sum += (byte >> i) & 1
        return sum

    def set_green_msbs_to_one(self):
        new_image = bytearray()
        for channel in range(self.channel_nbr):
            for y in range(self.height):
                for x in range(self.width):
                    if channel == 1:
                        byte = self.get_value(x, y, channel)
                        byte = byte | 0b10000000
                        new_image.append(byte)
                    else:
                        new_image.append(self.get_value(x, y, channel))
        return new_image

    def set_blue_lsbs_to_zero(self):
        new_image = bytearray()
        for channel in range(self.channel_nbr):
            for y in range(self.height):
                for x in range(self.width):
                    if channel == 2:
                        byte = self.get_value(x, y, channel)
                        byte = byte & 0b11111110
                        new_image.append(byte)
                    else:
                        new_image.append(self.get_value(x, y, channel))
        return new_image

    def set_unsigned(self):
        new_image = bytearray()
        for channel in range(self.channel_nbr):
            for y in range(self.height):
                for x in range(self.width):
                    byte = self.get_value(x, y, channel)
                    byte1 = 0x00
                    byte2 = byte - (byte >> 15 << 16)
                    new_image.append(byte1)
                    new_image.append(byte2)
        new_image[0] = 0x00
        new_image[1] = 0x00

        new_image[2 * self.width * self.height] = 0xFF
        new_image[2 * self.width * self.height + 1] = 0xFF

        return new_image

    def get_bytes_histogram_of_channel(self, channel):
        d = {}
        for y in range(self.height):
            for x in range(self.width):
                byte = self.get_value(x, y, channel)
                d[byte] = d.get(byte, 0) + 1
        d = dict(sorted(d.items()))
        return d

    def get_bytes_histogram(self):
        d = {}
        for channel in range(self.channel_nbr):
            d = Counter(d) + Counter(self.get_bytes_histogram_of_channel(channel))
        return d

    def get_linked_bytes_histogram(self):
        d = {}
        for channel in range(self.channel_nbr):
            for y in range(self.height):
                for x in range(self.width):
                    byte = self.get_value(x, y, channel)
                    current_byte_dict = d.get(byte, {})
                    previous_byte_value = self.get_value(x - 1, y, channel)
                    current_byte_dict[previous_byte_value] = (
                        current_byte_dict.get(previous_byte_value, 0) + 1
                    )
                    d[byte] = current_byte_dict
        d = dict(sorted(d.items()))
        return d

    def get_jpeg_compressed(self):
        return ricse.compress_raw_with_jpeg(
            self.path, "./compressed.jpg", "reconstructed.jpg", 1
        )

    def add_ppm_header(self, path):
        with open(path, "rb") as f:
            header = bytearray(f.read())
        self.data = header + self.data

    def write(self, path):
        with open(path, "wb") as f:
            f.write(self.data)
