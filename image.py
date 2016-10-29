import os
import zlib
import gzip
from StringIO import StringIO

# prints 256 colors
for i in range(256):
    print("\033["+str(i)+"mx\033[0m")

IMAGE_DEBUG = False

class Commons(object):

    def _chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in xrange(0, len(l), n):
            yield l[i:i + n]

    def bytes2int(self, data):
        try:
            return int(data.encode('hex'), 16)
        except ValueError:
            return None

    def decompress(self, frmt, data):
        return {
            'gz': lambda :zlib.decompress(data, zlib.MAX_WBITS|16),
            'zlib': lambda :zlib.decompress(data),
            'deflate': lambda :zlib.decompress(data, -zlib.MAX_WBITS)
        }[frmt]()

class PortableNetworkGraphics(Commons):

    def __init__(self, path):
        with open(path, 'rb') as f:
            self.blob = f
            self.file_header = self.blob.read(8)
            chunk_length_size = 4
            chunk_type_size = 4
            crc_size = 4
            self.chunks = {}
            while True:
                chunk_length = self.bytes2int(self.blob.read(
                    chunk_length_size))
                if not chunk_length:
                    break
                chunk_type = self.blob.read(chunk_type_size)
                chunk_data = self.blob.read(chunk_length)
                crc = self.blob.read(crc_size)
                self.chunks[chunk_type] = {
                    'type': chunk_type,
                    'data': chunk_data,
                    'crc': crc,
                    'is_critical': chunk_type[0].isupper()
                }
            IHDR = self.chunks['IHDR']['data']
            self.width = self.bytes2int(IHDR[0:4])  # 4 bytes
            self.height = self.bytes2int(IHDR[4:8])  # 4 bytes
            self.bit_depth = self.bytes2int(IHDR[8:9])  # 1 byte
            self.color_type = self.bytes2int(IHDR[9:10])  # 1 byte
            self.compression_method = self.bytes2int(IHDR[11:12])  # 1 byte
            self.filter_method = self.bytes2int(IHDR[13:14])  # 1 byte
            self.interlace_method =  self.bytes2int(IHDR[15:16])  # 1 byte
            # Palette
            try:
                PLTE = self.chunks['PLTE']['data']
                self.palette = []
                for chunk in list(self._chunks(PLTE, 3)):
                    self.palette.append({
                        'r': self.bytes2int(chunk),
                        'g': self.bytes2int(chunk),
                        'b': self.bytes2int(chunk)})
            except KeyError:
                pass  # Palette key not present
            # Pixel Array
            IDAT = self.chunks['IDAT']['data']
            self.decompress('zlib', IDAT)
            #try:  # uncompressing gz
            #    with gzip.GzipFile(fileobj=StringIO(IDAT), mode='rb') as f:
            #        IDAT = f.read()
            #except Exception as e:
            #    print(e)
            self.pixels = []
            import binascii
            print('decompressing IDAT with bit depth {}'.format(self.bit_depth))
            for chunk in list(self._chunks(IDAT, self.bit_depth)):
                print('chunk <{}>'.format(chunk))
                self.pixels.append(chunk)
            print('{} pixels'.format(
                len(self.pixels)
                ))

    def _bit_depth_restrictions(self):
        '''
        Color    Allowed    Interpretation (Each pixel)
        Type    Bit Depths
       
        0  1,2,4,8,16 is a grayscale sample.
        2  8,16       is an R,G,B triple.
        3  1,2,4,8    is a palette index; a PLTE chunk must appear.
        4  8,16       is a grayscale sample,followed by an alpha sample.
        6  8,16       is an R,G,B triple, followed by an alpha sample.
        '''
        return reduce(lambda acc, new: acc or new, [
            self.color_type == 0 and self.bit_depth in [1, 2, 4, 8, 16],
            self.color_type == 2 and self.bit_depth in [8, 16],
            self.color_type == 3 and self.bit_depth in [1, 2, 4, 8],
            self.color_type == 4 and self.bit_depth in [8, 16],
            self.color_type == 6 and self.bit_depth in [8, 16]])

    def get_data(self):
        return self.chunks['IDAT']

filename = 'rubber-duck-small.png'
img = PortableNetworkGraphics('rubber-duck-small.png')
print(img.file_header)
print(img.chunks.keys())
print(
    '{} - data size {}'.format(filename, len(img.chunks['IDAT']['data']))
)
print('width {}'.format(img.width))
print('height {}'.format(img.height))
print('color type {}'.format(img.color_type))
print('interlace_method {}'.format(img.interlace_method))
