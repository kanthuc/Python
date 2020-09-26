"""
Implementation of an auto-balanced binary tree!
For doctests run following command:
python3 -m doctest -v avl_tree.py
For testing run:
python avl_tree.py
"""

import math
import random
from typing import Any, Optional


class Queue:
    def __init__(self) -> None:
        self.data = []
        self.head = 0
        self.tail = 0

    def is_empty(self) -> bool:
        return self.head == self.tail

    def push(self, data: Any) -> None:
        self.data.append(data)
        self.tail = self.tail + 1

    def pop(self) -> Any:
        ret = self.data[self.head]
        self.head = self.head + 1
        return ret

    def count(self) -> int:
        return self.tail - self.head

    def print(self) -> None:
        print(self.data)
        print("**************")
        print(self.data[self.head : self.tail])


class Node:
    def __init__(self, data: int) -> int:
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

    def get_data(self) -> int:
        return self.data

    def get_left(self) -> Optional["Node"]:
        return self.left

    def get_right(self) -> Optional["Node"]:
        return self.right

    def get_height(self) -> int:
        return self.height

    def set_data(self, data: int) -> None:
        self.data = data

    def set_left(self, node: "Node") -> None:
        self.left = node

    def set_right(self, node: "Node") -> None:
        self.right = node

    def set_height(self, height: int) -> None:
        self.height = height


def get_height(node: Node) -> int:
    if node is None:
        return 0
    return node.get_height()


def my_max(a: int, b: int) -> int:
    if a > b:
        return a
    return b


def right_rotation(node: Node) -> Node:
    r"""
            A                      B
           / \                    / \
          B   C                  Bl  A
         / \       -->          /   / \
        Bl  Br                 UB Br  C
       /
     UB
    UB = unbalanced node
    """
    print("left rotation node:", node.get_data())
    ret = node.get_left()
    node.set_left(ret.get_right())
    ret.set_right(node)
    h1 = my_max(get_height(node.get_right()), get_height(node.get_left())) + 1
    node.set_height(h1)
    h2 = my_max(get_height(ret.get_right()), get_height(ret.get_left())) + 1
    ret.set_height(h2)
    return ret


def left_rotation(node: Node) -> Node:
    """
    a mirror symmetry rotation of the left_rotation
    """
    print("right rotation node:", node.get_data())
    ret = node.get_right()
    node.set_right(ret.get_left())
    ret.set_left(node)
    h1 = my_max(get_height(node.get_right()), get_height(node.get_left())) + 1
    node.set_height(h1)
    h2 = my_max(get_height(ret.get_right()), get_height(ret.get_left())) + 1
    ret.set_height(h2)
    return ret


def lr_rotation(node: Node) -> Node:
    r"""
            A              A                    Br
           / \            / \                  /  \
          B   C    LR    Br  C       RR       B    A
         / \       -->  /  \         -->    /     / \
        Bl  Br         B   UB              Bl    UB  C
             \        /
             UB     Bl
    RR = right_rotation   LR = left_rotation
    """
    node.set_left(left_rotation(node.get_left()))
    return right_rotation(node)


def rl_rotation(node: Node) -> Node:
    node.set_right(right_rotation(node.get_right()))
    return left_rotation(node)


def insert_node(node: Node, data: int) -> Node:
    if node is None:
        return Node(data)
    if data < node.get_data():
        node.set_left(insert_node(node.get_left(), data))
        if (
            get_height(node.get_left()) - get_height(node.get_right()) == 2
        ):  # an unbalance detected
            if (
                data < node.get_left().get_data()
            ):  # new node is the left child of the left child
                node = right_rotation(node)
            else:
                node = lr_rotation(node)
    else:
        node.set_right(insert_node(node.get_right(), data))
        if get_height(node.get_right()) - get_height(node.get_left()) == 2:
            if data < node.get_right().get_data():
                node = rl_rotation(node)
            else:
                node = left_rotation(node)
    h1 = my_max(get_height(node.get_right()), get_height(node.get_left())) + 1
    node.set_height(h1)
    return node


def get_rightMost(root: Node) -> int:
    while root.get_right() is not None:
        root = root.get_right()
    return root.get_data()


def get_leftMost(root: Node) -> int:
    while root.get_left() is not None:
        root = root.get_left()
    return root.get_data()


def del_node(root: Node, data: int) -> Node:
    if root.get_data() == data:
        if root.get_left() is not None and root.get_right() is not None:
            temp_data = get_leftMost(root.get_right())
            root.set_data(temp_data)
            root.set_right(del_node(root.get_right(), temp_data))
        elif root.get_left() is not None:
            root = root.get_left()
        else:
            root = root.get_right()
    elif root.get_data() > data:
        if root.get_left() is None:
            print("No such data")
            return root
        else:
            root.set_left(del_node(root.get_left(), data))
    elif root.get_data() < data:
        if root.get_right() is None:
            return root
        else:
            root.set_right(del_node(root.get_right(), data))
    if root is None:
        return root
    if get_height(root.get_right()) - get_height(root.get_left()) == 2:
        if get_height(root.get_right().get_right()) > get_height(
            root.get_right().get_left()
        ):
            root = left_rotation(root)
        else:
            root = rl_rotation(root)
    elif get_height(root.get_right()) - get_height(root.get_left()) == -2:
        if get_height(root.get_left().get_left()) > get_height(
            root.get_left().get_right()
        ):
            root = right_rotation(root)
        else:
            root = lr_rotation(root)
    height = my_max(get_height(root.get_right()), get_height(root.get_left())) + 1
    root.set_height(height)
    return root


class AVLtree:
    """
    An AVL tree doctest
    Examples:
    >>> t = AVLtree()
    >>> t.insert(4)
    insert:4
    >>> print(str(t).replace(" \\n","\\n"))
     4
    *************************************
    >>> t.insert(2)
    insert:2
    >>> print(str(t).replace(" \\n","\\n").replace(" \\n","\\n"))
      4
     2  *
    *************************************
    >>> t.insert(3)
    insert:3
    right rotation node: 2
    left rotation node: 4
    >>> print(str(t).replace(" \\n","\\n").replace(" \\n","\\n"))
      3
     2  4
    *************************************
    >>> t.get_height()
    2
    >>> t.del_node(3)
    delete:3
    >>> print(str(t).replace(" \\n","\\n").replace(" \\n","\\n"))
      4
     2  *
    *************************************
    """

    def __init__(self) -> None:
        self.root = None

    def get_height(self) -> int:
        #        print("yyy")
        return get_height(self.root)

    def insert(self, data: int) -> None:
        print("insert:" + str(data))
        self.root = insert_node(self.root, data)

    def del_node(self, data: int) -> None:
        print("delete:" + str(data))
        if self.root is None:
            print("Tree is empty!")
            return
        self.root = del_node(self.root, data)

    def __str__(self) -> str:
        """
        a level traversale, gives a more intuitive look on the tree
        """

        output = ""
        q = Queue()
        q.push(self.root)
        layer = self.get_height()
        if layer == 0:
            return output
        cnt = 0
        while not q.is_empty():
            node = q.pop()
            space = " " * int(math.pow(2, layer - 1))
            output += space
            if node is None:
                output += "*"
                q.push(None)
                q.push(None)
            else:
                output += str(node.get_data())
                q.push(node.get_left())
                q.push(node.get_right())
            output += space
            cnt = cnt + 1
            for i in range(100):
                if cnt == math.pow(2, i) - 1:
                    layer = layer - 1
                    if layer == 0:
                        output += "\n*************************************"
                        return output
                    output += "\n"
                    break
        output += "\n*************************************"
        return output


def _test() -> None:
    import doctest

    doctest.testmod()


if __name__ == "__main__":
    _test()
    t = AVLtree()
    lst = list(range(10))
    random.shuffle(lst)
    for i in lst:
        t.insert(i)
        print(str(t))
    random.shuffle(lst)
    for i in lst:
        t.del_node(i)
        print(str(t))
