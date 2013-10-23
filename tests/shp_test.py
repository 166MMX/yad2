import unittest
from yad2.formats import Shp
from base64 import b64decode, b64encode

class ShpHeaderTest(unittest.TestCase):

    def chunk_header_test(self):
        header = Shp.Chunk.Header(b64decode("AAAQEAAQZQBuAA=="))
        self.assertEqual(header.flags, 0)
        self.assertEqual(header.datasize, 110)
        self.assertEqual(header.height, 16)
        
    def chunk_data_test(self):
        pass
