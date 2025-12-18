import struct
import zlib

def write_png(filename, width, height, color):
    # color is (r, g, b)
    def pack_chunk(tag, data):
        to_check = tag + data
        return struct.pack("!I", len(data)) + to_check + struct.pack("!I", zlib.crc32(to_check) & 0xFFFFFFFF)

    with open(filename, 'wb') as f:
        # PNG Header
        f.write(b'\x89PNG\r\n\x1a\n')

        # IHDR Chunk
        f.write(pack_chunk(b'IHDR', struct.pack("!IIBBBBB", width, height, 8, 2, 0, 0, 0)))

        # IDAT Chunk
        # Raw data: (1 byte filter + width * 3 bytes rgb) * height
        raw_data = b''
        row_data = b'\x00' + struct.pack("BBB", *color) * width
        raw_data = row_data * height

        f.write(pack_chunk(b'IDAT', zlib.compress(raw_data)))

        # IEND Chunk
        f.write(pack_chunk(b'IEND', b''))

# Deep Forest Green #2A4434 -> (42, 68, 52)
write_png('icon-192.png', 192, 192, (42, 68, 52))
write_png('icon-512.png', 512, 512, (42, 68, 52))
print("Icons created successfully.")
