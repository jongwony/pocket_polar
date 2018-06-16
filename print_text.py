import os
import sys
import struct

# TODO: make state machine like typewriter
bold = 1
underscore = 1
content = 'test!'.encode('cp949')
w = 0
h = 0
size = w & 0xF | h << 4 & 0xF0
align = 0

f = os.open('/dev/tty.WOOSIM-BTSERIAL', os.O_WRONLY)
s_init = struct.pack('2b', 27, 64)
s_style = struct.pack('12b', 27, 69, bold, 27, 45, underscore, 29, 66, 0,
                      29, 33, size)
s_align = struct.pack('3b', 27, 97, align)
s_end = struct.pack('b', 10)

s = s_init
s += s_style
s += s_align
s += content
s += b'\r\n' * 3
s += s_end

# TODO: when this binary string flushing?
print(s)
os.write(f, s)
os.close(f)
