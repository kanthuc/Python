class FenwickTree:
    def __init__(self, SIZE: int) -> None:  # create fenwick tree with size SIZE
        self.Size = SIZE
        self.ft = [0 for i in range(0, SIZE)]

    def update(
        self, i: int, val: int
    ) -> None:  # update data (adding) in index i in O(lg N)
        while i < self.Size:
            self.ft[i] += val
            i += i & (-i)

    def query(self, i: int) -> int:
        """
        query cumulative data from index 0 to i in O(lg N)
        >>> f = FenwickTree(100)
        >>> f.update(1, 20)
        >>> f.update(4, 4)
        >>> f.query(1)
        20
        >>> f.query(3)
        20

        >>> f.update(2, -5)
        >>> f.query(1)
        20
        >>> f.query(3)
        15
        """
        ret = 0
        while i > 0:
            ret += self.ft[i]
            i -= i & (-i)
        return ret


if __name__ == "__main__":
    f = FenwickTree(100)
    f.update(1, 20)
    f.update(4, 4)
    print(f.query(1))
    print(f.query(3))
    print(f.query(4))
    f.update(2, -5)
    print(f.query(1))
    print(f.query(3))
