#!/bin/env/python

## ql-demo-parse.py
## Shawn Nock, 2014

import struct
from bitarray import bitarray

class HuffNode:
    symbol=None
    weight=0
    NYT=False
    
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
        global root
        if self == root:
            return True
        return False
    def __repr__(self):
        return "<Code: %s; Symbol: %s; Weight: %s; Root: %s; Leaf: %s; NYT: %s>"%(self.encode(), self.symbol, self.weight, self.is_root(), self.is_leaf(), self.NYT)

root=HuffNode()
root.NYT=True
nodes = {}

def huff_swap(node, node2):
    assert not node == root or node2 == root
        
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
    while not node == None:
        # Initialize list if non-existant
        print("Updating: %s" % node)
        if not node.weight+1 in nodes:
            nodes[node.weight+1]=[]
        ## Swap with highest priority non-parent by weight
        for rival in nodes[node.weight+1]:
            if rival == node.parent:
                continue
            if rival == root or node == root:
                continue
            huff_swap(node, rival)
            break
        # Remove from previous weight class
        if node.weight in nodes and node in nodes[node.weight]:
            nodes[node.weight].remove(node)
            # Clean up empty lists
            #if nodes[node.weight] == []:
            #    del nodes[node.weight]
        
        # Increment the weight and insert at the head of new weight
        # class
        node.weight +=1
        nodes[node.weight].insert(0, node)
        node=node.parent

def huff_update_tree_new(node):
    while not node == None:
        if not node.parent:
            node.weight += 1
            break
        rival = node.parent.left if node.parent.right == node else node.parent.right
        if node.weight+1 > rival.weight:
            huff_swap(rival, node)
        node.weight +=1
        node=node.parent
        
def huff_add_node(symbol, NYT):
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

    huff_update_tree_new(NYT.parent)

def huff_read_block(block):
    global root
    node=root
    buf=bitarray()
    pos=0

    while pos <= len(block) - 1:
        bit = block[pos]
        pos += 1
        if node.NYT:
            # We're at the NYT, add a leaf
            print("Received NYT")
            symbol = block[pos:pos+8]
            pos+=8
            NYT=huff_add_node(symbol,node)
            buf.append(symbol)
            node=root
            continue
        if node.is_leaf():
            symbol = node.symbol
            print("Symbol hit: %s" % symbol)
            buf+=node.symbol
            huff_update_tree_new(node)
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
            break

if __name__ == '__main__':
    main()


