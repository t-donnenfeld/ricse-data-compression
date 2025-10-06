# Exercise 2.1 : Quizz Data I/O
# Exercise 2.2 :
# pixel(100,200) : 179, 195, 136


class RawImage:
    def __init__(self, path, width, height, channel_nbr, data_type) -> None:
        self.width = width
        with open(path, "rb") as f:
            self.data = bytearray(f.read())
        self.height = height
        self.channel_nbr = channel_nbr
        self.data_type = data_type

    def set_value_in_channel(self, x, y, channel, value):
        offset = (y * self.width + x) + channel * self.width * self.height
        self.data[offset] = value

    def get_value_in_channel(self, x, y, channel):
        offset = (y * self.width + x) + channel * self.width * self.height
        return self.data[offset]

    def get_values(self, x, y):
        return [self.get_value_in_channel(x, y, i) for i in range(self.channel_nbr)]

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
                        byte = self.get_value_in_channel(x, y, channel)
                        byte = byte | 0b10000000
                        new_image.append(byte)
                    else:
                        new_image.append(
                            self.get_value_in_channel(x, y, channel))
        return new_image

    def set_blue_lsbs_to_zero(self):
        new_image = bytearray()
        for channel in range(self.channel_nbr):
            for y in range(self.height):
                for x in range(self.width):
                    if channel == 2:
                        byte = self.get_value_in_channel(x, y, channel)
                        byte = byte & 0b11111110
                        new_image.append(byte)
                    else:
                        new_image.append(
                            self.get_value_in_channel(x, y, channel))
        return new_image

    def set_unsigned(self):
        new_image = bytearray()
        for channel in range(self.channel_nbr):
            for y in range(self.height):
                for x in range(self.width):
                    byte = self.get_value_in_channel(x, y, channel)
                    byte1 = 0x00
                    byte2 = byte - (byte >> 15 << 16)
                    new_image.append(byte1)
                    new_image.append(byte2)
        new_image[0] = 0x00
        new_image[1] = 0x00

        new_image[2 * self.width * self.height] = 0xFF
        new_image[2 * self.width * self.height + 1] = 0xFF

        return new_image


if __name__ == "__main__":
    mandrill = RawImage("./4_mandrill-u8be-3x512x512.raw", 512, 512, 3, "u8be")
    # print(mandrill.get_value_in_channel(100, 200, 2))
    # print(mandrill.get_values(100, 200))
    # print(mandrill.count_true_bits())
    with open("unsignedmonkey", "wb") as f:
        f.write(mandrill.set_unsigned())
