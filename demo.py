#!/bin/env/python

## ql-demo-parse.py
## Shawn Nock, 2014

import struct
from bitarray import bitarray

class HuffNode:
    symbol=None
    weight=0
    
    left=None
    right=None
    parent=None

    def is_leaf(self):
        if not self.left and not self.right:
            return True
        return False
    def is_root(self):
        global root
        if self == root:
            return True
        return False
    def __repr__(self):
        return "<Symbol: %s; Weight: %s; Root: %s; Leaf: %s>"%(self.symbol, self.weight, self.is_root(), self.is_leaf())

root=HuffNode()
NYT=root
nodes = {}
nodes[root.weight] = [root]
        
def huff_swap(node, node2):
    if node.is_root() or node2.is_root():
        return
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
    ## Starting with node, backtrack the tree incrementing weights and
    ## adapting the tree as needed
    need_update=[]
    while node is not None:
        need_update.append(node)
        node=node.parent
    for node in need_update:
        if not node.weight+1 in nodes:
            nodes[node.weight+1]=[node]
        else:
            if not node.parent == nodes[node.weight+1][0]:
                huff_swap(node, nodes[node.weight+1][0])
                nodes[node.weight+1].insert(0, node)
        if node.weight in nodes and node in nodes[node.weight]:
            nodes[node.weight].remove(node)
            if nodes[node.weight] == []:
                del nodes[node.weight]
        node.weight +=1
        
def huff_add_node(symbol):
    left=HuffNode()
    right=HuffNode()

    global NYT

    NYT.left=left
    NYT.right=right
    
    left.parent = NYT
    left.symbol = None

    right.parent = NYT
    right.symbol = symbol

    NYT=left
    
    huff_update_tree(right)

def huff_read_block(block):
    node=root
    buf=bitarray()
    pos=0

    while pos <= len(block) - 1:
        bit = block[pos]
        pos += 1
        if node == NYT:
            # We're at the NYT, add a leaf
            print("Received NYT")
            symbol = block[pos:pos+8]
            pos+=8
            huff_add_node(symbol)
            buf.append(symbol)
            node=root
            continue
        if node.is_leaf():
            symbol = node.symbol
            print("Symbol hit: %s" % symbol)
            buf+=node.symbol
            huff_update_tree(node)
            node=root
            continue
        if bit:
            node=node.right
        else:
            node=node.left
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
    d = Demo()
    d.load('test.dm_73')
    with open('output', 'wb') as ff:
        for block in d.blocks:
            huff_read_block(block[2]).tofile(ff)
            ff.flush()

if __name__ == '__main__':
    main()


