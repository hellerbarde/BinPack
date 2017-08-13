#!/usr/bin/env python
"""
BinTree Class:

2 dimensional Bin Packing Data Structure

BinTrees have right and bottom children. Items
are inserted using recursion to find the first
open BinTree unoccupied node large enough to fit
them Item. That node is resized to match the Item
and child nodes are created to fill the unused
space to the left.

Example:
    Item := (2,4)
    Tree := ((4,8), occoupied == False)

    After Insertion:
    Tree :=     ((2,4), occupied == True)
                /                     \
      ((4,4), occupied == False)  ((2,4), occupied == False)

Items are namedtuples with x and y values. When
Items are inserted into a bin tree, insert()
recurses over child nodes until it finds the first
unoccupied node that fits the Item. The node is
resized to Item and two child nodes are created
to take up the remaining space to the right and
below the item.
"""

from typing import NamedTuple
from collections import deque

class CornerPoint(NamedTuple):
    """
    namedtuple representing the top left corner of each
    BinTree object.
    """
    x: int
    y: int


class Item(NamedTuple):
    """
    namedtuple representing objects added to BinTree.
    """
    width: int
    height: int


class BinTree:
    """
    Each BinTree instance has two children (left and bottom)
    and width (int), height (int), and occupied (bool) properties.
    """
    def __init__(self, dims: tuple = (4, 8)) -> None:
        self.corner = CornerPoint(0, 0)
        self.dims = dims
        self.occupied = False
        self.children = {i: None for i in range(len(dims))}
        self.parent = None
        if not self.occupied:
            self.largest_child = tuple(self.dims)
        else:
            self.largest_child = None


    def _check_dim(self, item_dim: int, bin_dim: int) -> bool:
        """
        Checks if the item will fit the bin in the specified
        dimension.
        """
        if bin_dim - item_dim > 0:
            return True
        return False


    def insert(self, item: tuple) -> bool:
        """
        Recursive item insertion
        Takes an Item namedtuple
        Inserts recursively as a side-effect
        Returns True or False if Item fit in bin
        """
        if not self.occupied and item.width <= self.dims[0] and item.height <= self.dims[1]:
            if self._check_dim(item[0], self.dims[0]):
                self.children[0] = BinTree(dims=[self.dims[0]-item[0], item[1]])
                self.children[0].parent = self
            if self.dims[1] - item[1] > 0:
                self.children[1] = BinTree(dims=[self.dims[0], self.dims[1]-item[1]])
                self.children[1].parent = self
            self.dims = (item.width, item.height)
            self.occupied = item
            if self.children[0]:
                self.children[0].corner = CornerPoint(self.dims[0] + self.corner.x, self.corner.y)
            if self.children[1]:
                self.children[1].corner = CornerPoint(self.corner.x, self.dims[1] + self.corner.y)
            self.calc_largest_child()
            return True
        else:
            if (self.children[0] and self.children[0].largest_child[0] >= item.width and
                    self.children[0].largest_child[1] >= item.height):
                self.children[0].insert(item)
            elif (self.children[1] and self.children[1].largest_child[0] >= item.width and
                  self.children[1].largest_child[1] >= item.height):
                self.children[1].insert(item)
            else:
                return False


    def calc_largest_child(self) -> None:
        """
        Updates self.largest_child for each node recursively
        back to the root node
        """
        choices = []
        if not self.occupied:
            choices.append(self.dims)
        else:
            choices.append((0, 0))
        if self.children[0]:
            choices.append(self.children[0].largest_child)
        else:
            choices.append((0, 0))
        if self.children[1]:
            choices.append(self.children[1].largest_child)
        else:
            choices.append((0, 0))
        self.largest_child = max(choices, key=lambda t: t[0]*t[1])

        if self.parent:
            self.parent.calc_largest_child()


def bin_stats(root: BinTree) -> dict:
    """
    Returns a dictionary with compiled stats on the bin tree
    """
    stats = {
                'width': 0,
                'height': 0,
                'area': 0,
                'efficiency': 1.0,
                'items': [],
            }

    stack = deque([root])
    while stack:
        node = stack.popleft()
        stats['width'] += node.dims[0]
        if node.children[0]:
            stack.append(node.children[0])

    stack = deque([root])
    while stack:
        node = stack.popleft()
        stats['height'] += node.dims[1]
        if node.children[1]:
            stack.append(node.children[1])

    stats['area'] = stats['width'] * stats['height']

    stack = deque([root])
    occupied = 0
    while stack:
        node = stack.popleft()
        if node.occupied:
            stats['items'].append((node.corner, node.occupied))
            occupied += node.dims[0]*node.dims[1]

        if node.children[0]:
            stack.append(node.children[0])
        if node.children[1]:
            stack.append(node.children[1])
    stats['efficiency'] = occupied / stats['area']
    return stats


if __name__ == '__main__':
    ROOT = BinTree()
    ITEM1 = Item(width=4, height=4)
    ITEM2 = Item(width=2, height=4)
    ITEM3 = Item(width=2, height=2)
    ITEM4 = Item(width=2, height=2)
    ROOT.insert(ITEM1)
    ROOT.insert(ITEM2)
    #ROOT.insert(ITEM3)
    ##ROOT.insert(ITEM4)
    print(bin_stats(ROOT))
    print(ROOT.children)


