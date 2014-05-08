#!/bin/env/python

## ql-demo-parse.py
## Shawn Nock, 2014

import struct
from bitarray import bitarray
from binascii import unhexlify
from copy import deepcopy

class HuffNode:
    symbol=None
    weight=0
    NYT=False
    
    ## Tree Structures
    left=None
    right=None
    parent=None

    def encode(self):
        code=bitarray()
        node=self
        while not node.is_root():
            if node.parent.left == node:
                code = bitarray('0') + code
            else:
                code = bitarray('1') + code
            node=node.parent
        return code

    def is_leaf(self):
        if not self.left and not self.right:
            return True
        return False
    def is_root(self):
        if self.parent == None:
            return True
        return False
    def __repr__(self):
        if self.is_leaf():
            return "Symbol: %s; Code: %s"%(self.symbol, self.encode())
        return "INTERNAL_NODE"
        #return "<Code: %s; Symbol: %s; Weight: %s; Root: %s; Leaf: %s; NYT: %s>"%(self.encode(), self.symbol, self.weight, self.is_root(), self.is_leaf(), self.NYT)


nodes = {}

huff_init_counts = [
       0x3D1CB, 0x0A0E9, 0x01894, 0x01BC2, 0x00E92, 0x00EA6, 0x017DE, 0x05AF3,

       0x08225, 0x01B26, 0x01E9E, 0x025F2, 0x02429, 0x0436B, 0x00F6D, 0x006F2,

       0x02060, 0x00644, 0x00636, 0x0067F, 0x0044C, 0x004BD, 0x004D6, 0x0046E,

       0x006D5, 0x00423, 0x004DE, 0x0047D, 0x004F9, 0x01186, 0x00AF5, 0x00D90,

       0x0553B, 0x00487, 0x00686, 0x0042A, 0x00413, 0x003F4, 0x0041D, 0x0042E,

       0x006BE, 0x00378, 0x0049C, 0x00352, 0x003C0, 0x0030C, 0x006D8, 0x00CE0,

       0x02986, 0x011A2, 0x016F9, 0x00A7D, 0x0122A, 0x00EFD, 0x0082D, 0x0074B,

       0x00A18, 0x0079D, 0x007B4, 0x003AC, 0x0046E, 0x006FC, 0x00686, 0x004B6,

       0x01657, 0x017F0, 0x01C36, 0x019FE, 0x00E7E, 0x00ED3, 0x005D4, 0x005F4,

       0x008A7, 0x00474, 0x0054B, 0x003CB, 0x00884, 0x004E0, 0x00530, 0x004AB,

       0x006EA, 0x00436, 0x004F0, 0x004F2, 0x00490, 0x003C5, 0x00483, 0x004A2,

       0x00543, 0x004CC, 0x005F9, 0x00640, 0x00A39, 0x00800, 0x009F2, 0x00CCB,

       0x0096A, 0x00E01, 0x009C8, 0x00AF0, 0x00A73, 0x01802, 0x00E4F, 0x00B18,

       0x037AD, 0x00C5C, 0x008AD, 0x00697, 0x00C88, 0x00AB3, 0x00DB8, 0x012BC,

       0x00FFB, 0x00DBB, 0x014A8, 0x00FB0, 0x01F01, 0x0178F, 0x014F0, 0x00F54,

       0x0131C, 0x00E9F, 0x011D6, 0x012C7, 0x016DC, 0x01900, 0x01851, 0x02063,

       0x05ACB, 0x01E9E, 0x01BA1, 0x022E7, 0x0153D, 0x01183, 0x00E39, 0x01488,

       0x014C0, 0x014D0, 0x014FA, 0x00DA4, 0x0099A, 0x0069E, 0x0071D, 0x00849,

       0x0077C, 0x0047D, 0x005EC, 0x00557, 0x004D4, 0x00405, 0x004EA, 0x00450,

       0x004DD, 0x003EE, 0x0047D, 0x00401, 0x004D9, 0x003B8, 0x00507, 0x003E5,

       0x006B1, 0x003F1, 0x004A3, 0x0036F, 0x0044B, 0x003A1, 0x00436, 0x003B7,

       0x00678, 0x003A2, 0x00481, 0x00406, 0x004EE, 0x00426, 0x004BE, 0x00424,

       0x00655, 0x003A2, 0x00452, 0x00390, 0x0040A, 0x0037C, 0x00486, 0x003DE,

       0x00497, 0x00352, 0x00461, 0x00387, 0x0043F, 0x00398, 0x00478, 0x00420,

       0x00D86, 0x008C0, 0x0112D, 0x02F68, 0x01E4E, 0x00541, 0x0051B, 0x00CCE,

       0x0079E, 0x00376, 0x003FF, 0x00458, 0x00435, 0x00412, 0x00425, 0x0042F,

       0x005CC, 0x003E9, 0x00448, 0x00393, 0x0041C, 0x003E3, 0x0042E, 0x0036C,

       0x00457, 0x00353, 0x00423, 0x00325, 0x00458, 0x0039B, 0x0044F, 0x00331,

       0x0076B, 0x00750, 0x003D0, 0x00349, 0x00467, 0x003BC, 0x00487, 0x003B6,

       0x01E6F, 0x003BA, 0x00509, 0x003A5, 0x00467, 0x00C87, 0x003FC, 0x0039F,

       0x0054B, 0x00300, 0x00410, 0x002E9, 0x003B8, 0x00325, 0x00431, 0x002E4,

       0x003F5, 0x00325, 0x003F0, 0x0031C, 0x003E4, 0x00421, 0x02CC1, 0x034C0]


def huff_init(root):
    NYT=root
    nodes_init={}
    for i in range(256):
        print(i)
        symbol = bytes(range(i,i+1))
        NYT = huff_add_node(symbol, NYT)
        nodes_init[i] = NYT.parent.right
        for j in range(huff_init_counts[i]-1):
            huff_update_tree(nodes_init[i])

def huff_swap(node, node2):
    parent=node.parent
    parent2=node2.parent
    node.parent = parent2
    node2.parent = parent

    if parent:
        if parent.left == node:
            parent.left = node2
        else:
            parent.right = node2

    if parent2:
        if parent2.left == node2:
            parent2.left = node
        else:
            parent2.right = node

    print("Swapped %s and %s"%(node, node2))

def huff_update_tree(node):
    if not node:
        return
    if node.parent:
        rivals = [node.parent.left if node.parent.right == node else node.parent.right]
        if node.parent.parent:
            rivals.append(node.parent.parent.left if node.parent.parent.right == node.parent else node.parent.parent.right)
        for rival in rivals:
            if node.weight == rival.weight:
                huff_swap(rival, node)
        huff_update_tree(node.parent)
    node.weight +=1

        
def huff_add_node(symbol, NYT):
    ## Adds new node and returns new NYT
    assert NYT.NYT == True
    left=HuffNode()
    right=HuffNode()

    NYT.left=left
    NYT.right=right
    
    left.parent = NYT
    left.symbol = None
    left.NYT=True
    NYT.NYT=False
    NYT.weight = 1

    right.parent = NYT
    right.symbol = symbol
    right.weight = 1

    huff_update_tree(NYT.parent)
    return left

def huff_read_block(root, block):
    node=root
    buf=bytes()
    pos=0

    while pos <= len(block) - 1:
        while not node.is_leaf():
            # Should never happen
            if pos > len(block) - 1:
                print(pos, len(block))
                return buf
            print(pos,len(block))
            bit = block[pos]
            pos += 1
            if bit:
                node=node.right
            else:
                node=node.left
        if node.is_leaf() and node.NYT:
            # We're at the NYT, add leaves
            print("Received NYT")
            symbol = block[pos:pos+8].tobytes()
            pos+=8
            NYT=huff_add_node(symbol,node)
            buf+=symbol
        else:
            symbol = node.symbol
            print("Symbol hit: %s" % symbol)
            buf+=node.symbol
            huff_update_tree(node)
        node=root
    return buf
 
class Demo:
    blocks = []

    def load(self, filename):
        with open(filename, 'rb') as f:
            while True:
                seq, length = struct.unpack('ii', f.read(8))
                if seq == -1 or length == -1:
                    break
                data = bitarray()
                data.frombytes(f.read(length))
                self.blocks.append([seq, length, data])

class DemoError(IOError):
    def __init__(self, msg):
        IOError.__init__(self)

def main():
    troot=HuffNode()
    troot.NYT=True
    huff_init(troot)
    d = Demo()
    d.load('test.dm_73')
    with open('output', 'wb') as ff:
        for block in d.blocks:
            root=deepcopy(troot)
            ff.write(huff_read_block(root, block[2]))
            ff.flush()


if __name__ == '__main__':
    main()


