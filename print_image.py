import os
import struct
from wand.image import Image

# FIXME: NOT WORK CURRENTLY
CAN = b'\x24'
DITHERING_FLOYD_STEINBERG = 2
DITHERING_NO = 0
DITHERING_RANDOM_THRESHOLD = 1
ESC = b'\x27'
GS = b'\x29'
MAX_RLE_LENGTH = 62
TAG = 'WoosimImage'
cmd_ESCFF = struct.pack('2B', 27, 12)
threshold = [0.25 + 0.01 * i for i in range(70 - 25)]


def gray_image(name):
    with Image(filename='profile.png') as img:
        img.type = 'grayscale'
        img.depth = 8
        img.resize(48, 20)
        width = img.width
        height = img.height
        blob = img.make_blob()

    # TODO: BMP? PNG? JPG?
    # pixels = b''
    # for i in range(0, width*height*3, 3):
    #     pixels += struct.pack('B', blob[i])

    return width, height, blob


def print_bmp():
    w_start = 0
    width = 384  # 48 * 8
    h_start = 0
    height = 200  # 25 * 8
    width_size = width // 8
    coloring = False, 0

    img_init = struct.pack('2B', 27, 76)
    img_data = struct.pack('2B 4H B B', 27, 87, w_start, h_start, width, height, 0, 10)

    # loop 373, 609
    if width % 8 == 0:
        if height > 0:
            img_data += struct.pack('2B 2x H B B', 27, 79, (width + 1) * 255 & 0xFF, 0, 5)

        # label 609
        img_data += struct.pack('5B B B', 27, 88, 52, width_size, height % 255, 0, 5)
        img_data += gray_image('profile_8.jpg')[2]
        img_data += struct.pack('2B', width_size * 255 & 0xFF, height % 255 * width_size & 0xFF)

    img_end = struct.pack('2B B B', 27, 12, 0, 2)

    img_end += struct.pack('2B', 27, 83)

    return img_init, img_data, img_end


def fast_print_bitmap():
    width, height, img = gray_image('profile_8.jpg')
    p1 = 0
    p2 = 0
    img_init = struct.pack('2b', 27, 87)
    img_init += struct.pack('4h', p1, p2, width, height)
    img_init += struct.pack('2b', 0, 10)
    img_init += struct.pack('3b', 27, 88, 52)
    img_init += struct.pack('2b', 48, 25)   # width // 8 * 255, height
    img_init += struct.pack('2b', 0, 5)
    img_data = img
    img_data += struct.pack('b b', 48, 25)
    # img_data += struct.pack('b b', width // 8 * 255 * height, width % 255 * width // 8)
    img_end = struct.pack('2b b b', 27, 12, 0, 2)
    img_end += struct.pack('b', 24)
    img_end += b'\r\n\r\n'

    return img_init, img_data, img_end


img_init, img_data, img_end = fast_print_bitmap()
f = os.open('/dev/tty.WOOSIM-BTSERIAL', os.O_WRONLY)
s = img_init
s += img_data
s += img_end

print(s)
os.write(f, s)
os.close(f)
